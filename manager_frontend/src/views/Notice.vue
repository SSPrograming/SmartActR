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
        <el-button type="primary" plain @click="handleCreate">新建公告</el-button>
      </div>
      <el-table class="table" :data="slicedData"
                :default-sort="{prop: 'noticeDate', order: 'descending'}">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="noticeDate" label="发布时间" width="150" sortable></el-table-column>
        <el-table-column prop="expireDate" label="过期时间" width="150" sortable></el-table-column>
        <el-table-column prop="noticeContent" label="概要" width="auto">
          <template slot-scope="scope">
            <el-scrollbar class="content">
              {{ scope.row.noticeContent }}
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
      noticeData: [],
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
      return this.noticeData.length
    },
    slicedData() {
      return this.noticeData.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage < this.noticeData.length ?
              this.pageSize * this.currentPage : this.noticeData.length)
    }
  },
  mounted() {
    this.noticeData = [
      {
        noticeID: 1,
        noticeDate: '2021-11-24',
        expireDate: '2021-11-31',
        noticeContent: '大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！'
      },
      {
        noticeID: 2,
        noticeDate: '2021-11-25',
        expireDate: '2021-11-31'
      },
      {
        noticeID: 3,
        noticeDate: '2021-11-26',
        expireDate: '2021-11-30'
      },
    ]
  },
  methods: {
    getNoticeList() {

    },
    showNumsChange(val) {
      this.showNums = val
    },
    queryStartDateChange(val) {
      this.queryStartDate = val
    },
    queryEndDateChange(val) {
      this.queryEndDate = val
    },
    queryStrChange(val) {
      this.queryStr = val
    },
    query() {

    },
    handleCreate() {
      this.editNoticeID = null
      this.form = {
        expireDate: null,
        noticeContent: '',
      }
      this.showNoticeEditor = true
    },
    handleEdit(row) {
      this.editNoticeID = row.noticeID
      this.showNoticeEditor = true
    },
    handleDelete(row) {
      console.log(row)
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
        expireDate: this.$utils.time.format(this.form.expireDate, 'yyyy-MM-dd'),
        noticeContent: this.form.noticeContent
      }
      this.dialogLoading = true
      if (!this.editNoticeID) {
        this.$api.notice.createNotice(params).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '创建成功', 'success')
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
        console.log('edit: ' + this.editNoticeID + '!')
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