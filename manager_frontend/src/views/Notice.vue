<template>
  <div class="notice">
    <el-dialog title="公告编辑" :visible.sync="showNoticeEditor" v-loading="dialogLoading">
      <NoticeEditor :form="form" @editorCancel="editorCancel" @editorConfirm="editorConfirm"></NoticeEditor>
    </el-dialog>
    <div class="container">
      <div class="toolbar">
        <Toolbar :show-nums="showNums" :query-start-date="queryStartDate" :query-end-date="queryEndDate"
                 :query-str="queryStr" choose-num choose-date query
                 @showNumsChange="showNumsChange" @queryStartDateChange="queryStartDateChange"
                 @queryEndDateChange="queryEndDateChange" @queryStrChange="queryStrChange" @query="query">
        </Toolbar>
        <el-button type="primary" plain @click="handleCreate">创建公告</el-button>
      </div>
      <el-table class="table" :data="slicedData" v-loading="tableLoading"
                :default-sort="{prop: 'postDate', order: 'descending'}">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="postDate" label="发布时间" width="150" sortable></el-table-column>
        <el-table-column prop="expireDate" label="过期时间" width="150" sortable></el-table-column>
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
      <el-pagination layout="prev, pager, next" :page-size="pageSize" :current-page.sync="currentPage"
                     :total="dataLength" background>
      </el-pagination>
    </div>
  </div>
</template>

<script>
import NoticeEditor from '../components/NoticeEditor'
import Toolbar from '../components/Toolbar'

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
      pageSize: 10,
      currentPage: 1,
      showNums: 20,
      queryStartDate: null,
      queryEndDate: null,
      queryStr: '',
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
    getNoticeList() {
      let params = {
        num: this.showNums,
        queryStartDate: this.queryStartDate && this.$utils.time.format(this.queryStartDate, 'yyyy-MM-dd'),
        queryEndDate: this.queryEndDate && this.$utils.time.format(this.queryEndDate, 'yyyy-MM-dd'),
        queryStr: this.queryStr
      }
      if (this.queryStartDate && this.queryEndDate && this.queryStr) {
        params = {
          ...params,
          queryType: 3
        }
      } else if (this.queryStartDate && this.queryEndDate) {
        delete params.queryStr
        params = {
          ...params,
          queryType: 1
        }
      } else if (this.queryStr) {
        delete params.queryStartDate
        delete params.queryEndDate
        params = {
          ...params,
          queryType: 2
        }
      } else {
        delete params.queryStartDate
        delete params.queryEndDate
        delete params.queryStr
        params = {
          ...params,
          queryType: 0
        }
      }
      this.tableLoading = true
      this.$api.notice.getNoticeList(params).then((res) => {
        if (res.data.errCode === 0) {
          this.noticeList = res.data.noticeList
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.tableLoading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.tableLoading = false
      })
    },
    showNumsChange(val) {
      this.showNums = val
      this.getNoticeList()
    },
    queryStartDateChange(val) {
      this.queryStartDate = val
      this.getNoticeList()
    },
    queryEndDateChange(val) {
      this.queryEndDate = val
      this.getNoticeList()
    },
    queryStrChange(val) {
      this.queryStr = val
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
      this.tableLoading = true
      this.$api.notice.deleteNotice({noticeID: row.noticeID}).then((res) => {
        if (res.data.errCode === 0) {
          this.$utils.alertMessage(this, '删除成功', 'success')
          this.getNoticeList()
        } else {
          this.$utils.error.APIError(this, res.data)
        }
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
      })
    },
    editorCancel() {
      this.showNoticeEditor = false
    },
    editorConfirm() {
      if (!this.form.expireDate) {
        this.$utils.alertMessage(this, '请设置过期时间', 'warning')
        return
      }
      let params = {
        expireDate: this.form.expireDate && this.$utils.time.format(this.form.expireDate, 'yyyy-MM-dd'),
        noticeContent: this.form.noticeContent
      }
      this.dialogLoading = true
      if (!this.editNoticeID) {
        this.$api.notice.createNotice(params).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '创建成功', 'success')
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

.toolbar {
  display: flex;
  justify-content: space-between;
}

.content {
  white-space: nowrap;
}

.table {
  margin: 10px auto 10px;
}

.delete {
  color: $--color-danger;

  &:focus, &:hover {
    color: mix($--color-danger, $--color-white, 75%);
  }

  &:active {
    color: $--color-danger;
  }
}

</style>