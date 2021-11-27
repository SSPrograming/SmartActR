<template>
  <div class="notice">
    <div class="container">
      <div class="toolbar">
        <Toolbar :show-nums="showNums" :query-start-date="queryStartDate" :query-end-date="queryEndDate"
                 :query-str="queryStr" choose-num choose-date query
                 @showNumsChange="showNumsChange" @queryStartDateChange="queryStartDateChange"
                 @queryEndDateChange="queryEndDateChange" @queryStrChange="queryStrChange">
        </Toolbar>
        <el-button type="primary" plain>新建公告</el-button>
      </div>
      <el-table class="table" :data="slicedData"
                :default-sort="{prop: 'noticeDate', order: 'descending'}" stripe>
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
import Toolbar from '../components/Toolbar';

export default {
  name: "Notice",
  components: {
    Toolbar
  },
  data() {
    return {
      noticeData: [],
      pageSize: 10,
      currentPage: 1,
      showNums: 20,
      queryStartDate: null,
      queryEndDate: null,
      queryStr: ''
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
    handleEdit(row) {
      console.log(row)
    },
    handleDelete(row) {
      console.log(row)
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