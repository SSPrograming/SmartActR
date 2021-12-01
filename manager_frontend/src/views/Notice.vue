<template>
  <div class="notice">
    <el-dialog title="公告编辑" :visible.sync="showNoticeEditor" v-loading="dialogLoading">
      <NoticeEditor :form="form" @editorCancel="editorCancel" @editorConfirm="editorConfirm"></NoticeEditor>
    </el-dialog>
    <div class="container">
      <div class="header">
        <Toolbar :toolbar="toolbar" choose-num choose-date query
                 @query="query">
        </Toolbar>
        <el-button type="primary" plain @click="handleCreate">创建公告</el-button>
      </div>
      <el-table class="table" :data="slicedData" v-loading="tableLoading" @sort-change="doSort"
                :default-sort="{prop: 'noticeID', order: 'descending'}">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="postDate" label="发布时间" width="150" :sortable="'custom'"></el-table-column>
        <el-table-column prop="expireDate" label="过期时间" width="150" :sortable="'custom'"></el-table-column>
        <el-table-column prop="content" label="概要" width="auto">
          <template slot-scope="scope">
            <el-scrollbar class="content">
              {{ scope.row.content }}
            </el-scrollbar>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" size="small" class="delete" @click="handleDelete(scope.row)"> 删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="pagination" layout="prev, pager, next" :page-size="pageSize"
                     :current-page.sync="currentPage" :total="dataLength" background>
      </el-pagination>
    </div>
  </div>
</template>

<script>
import NoticeEditor from '@/components/Editor/NoticeEditor'
import Toolbar from '@/components/Toolbar'

export default {
  name: "Notice",
  components: {
    NoticeEditor,
    Toolbar
  },
  data() {
    return {
      dialogLoading: false,
      tableLoading: false,
      noticeList: [{
        noticeID: 0,
        postDate: '',
        expireDate: '',
        content: ''
      }],
      sortType: {
        prop: 'noticeID',
        order: 'descending'
      },
      toolbar: {
        showNums: 20,
        queryStartDate: null,
        queryEndDate: null,
        queryStr: '',
      },
      pageSize: 10,
      currentPage: 1,
      editNoticeID: null,
      showNoticeEditor: false,
      form: {
        expireDate: null,
        noticeContent: '',
      }
    }
  },
  computed: {
    dataLength() {
      return this.noticeList.length
    },
    slicedData() {
      return this.noticeList.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage <= this.noticeList.length ?
              this.pageSize * this.currentPage : this.noticeList.length)
    }
  },
  mounted() {
    this.getNoticeList()
  },
  methods: {
    doSort(event) {
      if (event) {
        this.sortType.prop = event.prop
        this.sortType.order = event.order
      }
      if (!this.sortType.order) {
        this.sortType.prop = 'noticeID'
        this.sortType.order = 'descending'
      }
      this.$utils.sort(this.noticeList, this.sortType, 'noticeID')
    },
    getNoticeList() {
      let params = {
        num: this.toolbar.showNums
      }
      if (this.toolbar.queryStartDate && this.toolbar.queryEndDate && this.toolbar.queryStr) {
        if (this.toolbar.queryStartDate > this.toolbar.queryEndDate) {
          this.$utils.alertMessage(this, '请选择正确的时间区间', 'warning')
          return
        }
        params = {
          ...params,
          queryStartDate: this.toolbar.queryStartDate && this.$utils.time.format(this.toolbar.queryStartDate, 'yyyy-MM-dd'),
          queryEndDate: this.toolbar.queryEndDate && this.$utils.time.format(this.toolbar.queryEndDate, 'yyyy-MM-dd'),
          queryStr: this.toolbar.queryStr,
          queryType: 3
        }
      } else if (this.toolbar.queryStartDate && this.toolbar.queryEndDate) {
        if (this.toolbar.queryStartDate > this.toolbar.queryEndDate) {
          this.$utils.alertMessage(this, '请选择正确的时间区间', 'warning')
          return
        }
        params = {
          ...params,
          queryStartDate: this.toolbar.queryStartDate && this.$utils.time.format(this.toolbar.queryStartDate, 'yyyy-MM-dd'),
          queryEndDate: this.toolbar.queryEndDate && this.$utils.time.format(this.toolbar.queryEndDate, 'yyyy-MM-dd'),
          queryType: 1
        }
      } else if (this.toolbar.queryStr) {
        params = {
          ...params,
          queryStr: this.toolbar.queryStr,
          queryType: 2
        }
      } else {
        params = {
          ...params,
          queryType: 0
        }
      }
      this.tableLoading = true
      this.$api.notice.getNoticeList(params).then((res) => {
        if (res.data.errCode === 0) {
          this.noticeList = res.data.noticeList
          this.doSort()
          this.$utils.alertMessage(this, '获取数据成功', 'success')
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.tableLoading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.tableLoading = false
      })
    },
    query() {
      this.getNoticeList()
    },
    handleCreate() {
      if (this.editNoticeID) {
        this.editNoticeID = null
        this.form = {
          expireDate: null,
          noticeContent: '',
        }
      }
      this.showNoticeEditor = true
    },
    handleEdit(row) {
      this.editNoticeID = row.noticeID
      this.form = {
        expireDate: new Date(row.expireDate),
        noticeContent: row.content,
      }
      this.showNoticeEditor = true
    },
    handleDelete(row) {
      this.$confirm('此操作将删除该公告, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.tableLoading = true
        this.$api.notice.deleteNotice({noticeID: row.noticeID}).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '删除成功', 'success')
            this.getNoticeList()
          } else {
            this.$utils.error.APIError(this, res.data)
            this.tableLoading = false
          }
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.tableLoading = false
        })
      }).catch(() => {
      })
    },
    editorCancel() {
      this.showNoticeEditor = false
    },
    editorConfirm() {
      let params = {
        expireDate: this.form.expireDate && this.$utils.time.format(this.form.expireDate, 'yyyy-MM-dd'),
        noticeContent: this.form.noticeContent
      }
      this.dialogLoading = true
      if (!this.editNoticeID) {
        this.$api.notice.createNotice(params).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '创建成功', 'success')
            this.form = {
              expireDate: null,
              noticeContent: '',
            }
            this.getNoticeList()
          } else {
            this.$utils.error.APIError(this, res.data)
          }
          this.dialogLoading = false
          this.showNoticeEditor = false
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.dialogLoading = false
          this.showNoticeEditor = false
        })
      } else {
        params = {
          ...params,
          noticeID: this.editNoticeID
        }
        this.$api.notice.updateNotice(params).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '编辑成功', 'success')
            this.getNoticeList()
          } else {
            this.$utils.error.APIError(this, res.data)
          }
          this.dialogLoading = false
          this.showNoticeEditor = false
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.dialogLoading = false
          this.showNoticeEditor = false
        })
      }
    }
  }
}
</script>

<style scoped lang="scss">
@import "src/element-variables";

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: $--toolbar-margin-bottom;
}

.content {
  white-space: nowrap;
}

.pagination {
  margin-top: $--pagination-margin-top;
}

.delete {
  color: $--color-danger;

  &:focus, &:hover {
    color: mix($--color-danger, $--color-white, 75%);
  }

  &:active {
    color: mix($--color-danger, $--color-black, 75%);
  }
}

</style>