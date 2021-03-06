<template>
  <div class="notice">
    <el-dialog title="公告编辑" :visible.sync="showNoticeEditor" v-loading="dialogLoading">
      <NoticeEditor :form="form" @editorCancel="editorCancel" @editorConfirm="editorConfirm"></NoticeEditor>
    </el-dialog>
    <div class="container">
      <div class="header">
        <Toolbar :toolbar="toolbar" choose-num choose-date query @query="query"></Toolbar>
        <el-button type="primary" plain @click="handleCreate">创建公告</el-button>
      </div>
      <el-table class="table" :data="slicedData" v-loading="tableLoading" @sort-change="changeSortType"
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
            <el-button type="text" size="small" class="delete" @click="handleDelete(scope.row)">删除</el-button>
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
      toolbar: {
        showNums: 20,
        queryStartDate: null,
        queryEndDate: null,
        queryStr: '',
      },
      tableLoading: false,
      noticeList: [
        /*
        {
        noticeID: 0,
        postDate: '',
        expireDate: '',
        content: ''
        }
        */
      ],
      sortType: {
        prop: 'noticeID',
        order: 'descending'
      },
      pageSize: 10,
      currentPage: 1,
      dialogLoading: false,
      showNoticeEditor: false,
      form: {
        noticeID: null,
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
      this.doSort()
      return this.noticeList.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage <= this.noticeList.length ?
              this.pageSize * this.currentPage : this.noticeList.length)
    }
  },
  mounted() {
    this.getNoticeList()
  },
  methods: {
    changeSortType(event) {
      if (event) {
        this.sortType.prop = event.prop
        this.sortType.order = event.order
      }
      if (!this.sortType.order) {
        this.sortType.prop = 'noticeID'
        this.sortType.order = 'descending'
      }
    },
    doSort() {
      this.$utils.sort(this.noticeList, this.sortType, 'noticeID')
    },
    getNoticeList() {
      if (this.toolbar.queryStartDate && this.toolbar.queryEndDate &&
          this.toolbar.queryStartDate > this.toolbar.queryEndDate) {
        this.$utils.alertMessage(this, '请选择正确的时间区间', 'warning')
        return
      }
      let params = {
        num: this.toolbar.showNums
      }
      this.toolbar.queryStartDate && (params.queryStartDate = this.$utils.time.format(this.toolbar.queryStartDate, 'yyyy-MM-dd'))
      this.toolbar.queryEndDate && (params.queryEndDate = this.$utils.time.format(this.toolbar.queryEndDate, 'yyyy-MM-dd'))
      this.toolbar.queryStr && (params.queryStr = this.toolbar.queryStr)
      this.tableLoading = true
      this.$api.notice.getNoticeList(params).then((res) => {
        if (res.data.errCode === 0) {
          this.noticeList = res.data.noticeList
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
      if (this.form.noticeID) {
        this.form = {
          noticeID: null,
          expireDate: null,
          noticeContent: '',
        }
      }
      this.showNoticeEditor = true
    },
    handleEdit(row) {
      this.form = {
        noticeID: row.noticeID,
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
      // 创建
      if (!this.form.noticeID) {
        this.$api.notice.createNotice(params).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '创建成功', 'success')
            this.form = {
              noticeID: null,
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
      }
      // 编辑
      else {
        this.form.noticeID && (params.noticeID = this.form.noticeID)
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
  margin-bottom: $--pagination-margin-bottom;
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
