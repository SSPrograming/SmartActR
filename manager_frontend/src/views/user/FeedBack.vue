<template>
  <div class="feedback">
    <el-dialog title="反馈内容" :visible.sync="showFeedbackEditor">
      <FeedbackEditor :form="form" @editorCancel="showFeedbackEditor=false"
                      @editorConfirm="showFeedbackEditor=false"></FeedbackEditor>
    </el-dialog>
    <div class="header">
      <Toolbar :toolbar="toolbar" choose-num choose-date refresh @query="query" @refresh="getFeedbackList"></Toolbar>
    </div>
    <el-table class="table" :data="slicedData" v-loading="tableLoading" @sort-change="changeSortType"
              :default-sort="{prop: 'feedbackID', order: 'descending'}">
      <el-table-column type="index" width="50"></el-table-column>
      <el-table-column prop="postDate" label="提交时间" width="150" :sortable="'custom'"></el-table-column>
      <el-table-column prop="userName" label="提交人" width="150" :sortable="'custom'"></el-table-column>
      <el-table-column prop="feedbackContent" label="概要" width="auto">
        <template slot-scope="scope">
          <el-scrollbar class="content">
            {{ scope.row.feedbackContent }}
          </el-scrollbar>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleLookUp(scope.row)">查看详情</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination class="pagination" layout="prev, pager, next" :page-size="pageSize"
                   :current-page.sync="currentPage" :total="dataLength" background>
    </el-pagination>
  </div>
</template>

<script>
import Toolbar from '@/components/Toolbar'
import FeedbackEditor from '@/components/Editor/FeedbackEditor'

export default {
  name: "FeedBack",
  components: {
    FeedbackEditor,
    Toolbar
  },
  data() {
    return {
      tableLoading: false,
      toolbar: {
        showNums: 20,
        queryStartDate: null,
        queryEndDate: null,
      },
      feedbackList: [
        {
          feedbackID: 1,
          postDate: '2021-12-05',
          feedbackContent: '你们做得还不错嘛',
          userName: '美味しい'
        }
      ],
      sortType: {
        prop: 'feedbackID',
        order: 'descending'
      },
      pageSize: 10,
      currentPage: 1,
      showFeedbackEditor: false,
      form: {
        feedbackID: 1,
        postDate: '2021-12-05',
        feedbackContent: '你们做得还不错嘛',
        userName: '美味しい'
      }
    }
  },
  computed: {
    dataLength() {
      return this.feedbackList.length
    },
    slicedData() {
      this.doSort()
      return this.feedbackList.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage <= this.feedbackList.length ?
              this.pageSize * this.currentPage : this.feedbackList.length)
    }
  },
  methods: {
    changeSortType(event) {
      if (event) {
        this.sortType.prop = event.prop
        this.sortType.order = event.order
      }
      if (!this.sortType.order) {
        this.sortType.prop = 'feedbackID'
        this.sortType.order = 'descending'
      }
    },
    doSort() {
      this.$utils.sort(this.feedbackList, this.sortType, 'feedbackID')
    },
    getFeedbackList() {

    },
    query() {

    },
    handleLookUp(row) {
      this.form = row
      this.showFeedbackEditor = true
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

</style>
