<template>
  <div class="notice">
    <div class="container">
      <div class="header">
        <el-button type="primary" plain>新建公告</el-button>
      </div>
      <el-table class="table" :data="slicedData"
                :default-sort="{prop: 'noticeID', order: 'descending'}" stripe>
        <el-table-column prop="noticeID" label="ID" width="80"></el-table-column>
        <el-table-column prop="noticeTitle" label="标题" width="150"></el-table-column>
        <el-table-column prop="noticeDate" label="发布时间" width="200"></el-table-column>
        <el-table-column prop="expireDate" label="过期时间" width="200"></el-table-column>
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
export default {
  name: "Notice",
  data() {
    return {
      noticeData: [],
      pageSize: 10,
      currentPage: 1
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
        noticeTitle: '大家好',
        noticeDate: '2021-11-24',
        expireDate: '2021-11-31',
        noticeContent: '大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！'
      },
      {
        noticeID: 2,
        noticeTitle: '闲来没事',
        noticeDate: '2021-11-25',
        expireDate: '2021-11-31'
      },
      {
        noticeID: 3,
        noticeTitle: '玩游戏吧',
        noticeDate: '2021-11-26',
        expireDate: '2021-11-30'
      },
    ]
  },
  methods: {
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