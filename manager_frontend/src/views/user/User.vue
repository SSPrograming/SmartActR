<template>
  <div class="user">
    <div class="container">
      <div class="header">
        <el-input class="input-query" placeholder="请输入学生号" prefix-icon="el-icon-search"
                  v-model="toolbar.stuID" @keyup.enter.native="query">
        </el-input>
        <el-input class="input-query" placeholder="请输入学生姓名" prefix-icon="el-icon-search"
                  v-model="toolbar.stuName" @keyup.enter.native="query">
        </el-input>
        <el-input class="input-query" placeholder="请输入院系" prefix-icon="el-icon-search"
                  v-model="toolbar.department" @keyup.enter.native="query">
        </el-input>
        <el-button class="query-button" type="info" @click="query">查找</el-button>
      </div>
      <el-table class="table" :data="slicedData" v-loading="tableLoading" @sort-change="changeSortType"
                :default-sort="{prop: 'stuID', order: 'ascending'}">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="stuID" label="学生号" width="150" :sortable="'custom'"></el-table-column>
        <el-table-column prop="stuName" label="姓名" width="150" :sortable="'custom'"></el-table-column>
        <el-table-column prop="department" label="院系" width="180" :sortable="'custom'"></el-table-column>
        <el-table-column prop="cellphone" label="手机" width="200" :sortable="'custom'"></el-table-column>
        <el-table-column prop="email" label="邮箱" :sortable="'custom'"></el-table-column>
        <el-table-column prop="status" label="状态" width="150" :sortable="'custom'"></el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button type="text" size="small" class="freeze" @click="handleFreeze(scope.row)">冻结</el-button>
            <el-button type="text" size="small" class="unfreeze" @click="handleUnFreeze(scope.row)">解冻</el-button>
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
export default {
  name: "User",
  data() {
    return {
      toolbar: {
        stuID: '',
        stuName: '',
        department: ''
      },
      tableLoading: false,
      stuList: [{
        userID: '',
        stuID: '202020202',
        stuName: '水神',
        department: '摸鱼学院',
        email: 'happy@my.world',
        cellphone: '12345678900',
        status: '活跃'
      }],
      sortType: {
        prop: 'stuID',
        order: 'ascending'
      },
      pageSize: 10,
      currentPage: 1
    }
  },
  computed: {
    dataLength() {
      return this.stuList.length
    },
    slicedData() {
      this.doSort()
      return this.stuList.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage <= this.stuList.length ?
              this.pageSize * this.currentPage : this.stuList.length)
    }
  },
  methods: {
    changeSortType(event) {
      if (event) {
        this.sortType.prop = event.prop
        this.sortType.order = event.order
      }
      if (!this.sortType.order) {
        this.sortType.prop = 'stuID'
        this.sortType.order = 'ascending'
      }
    },
    doSort() {
      this.$utils.sort(this.stuList, this.sortType, 'stuID')
    },
    getStuList() {

    },
    query() {

    },
    handleFreeze(row) {
      this.$confirm('此操作将冻结该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log(row)
      }).catch(() => {
      })
    },
    handleUnFreeze(row) {
      this.$confirm('此操作将解冻该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log(row)
      }).catch(() => {
      })
    }
  }
}
</script>

<style scoped lang="scss">
@import "src/element-variables";

.header {
  display: flex;
  margin-bottom: $--toolbar-margin-bottom;

  .input-query {
    flex-basis: 200px;

    & + .input-query {
      margin-left: 5px;
    }
  }

  .query-button {
    margin-left: 5px;
  }
}

.pagination {
  margin-top: $--pagination-margin-top;
}

.freeze {
  color: steelblue;

  &:focus, &:hover {
    color: mix(steelblue, $--color-white, 75%);
  }

  &:active {
    color: mix(steelblue, $--color-black, 75%);
  }
}

.unfreeze {
  color: orange;

  &:focus, &:hover {
    color: mix(orange, $--color-white, 75%);
  }

  &:active {
    color: mix(orange, $--color-black, 75%);
  }
}

</style>