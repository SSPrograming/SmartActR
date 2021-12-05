<template>
  <div class="user">
    <div class="container">
      <div class="header">
        <el-select class="choose-num" v-model="toolbar.showNums" placeholder="请选择" @change="getStuList">
          <el-option v-for="item in numOptions" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
        <el-input class="input-query" placeholder="请输入学号" prefix-icon="el-icon-search"
                  v-model="toolbar.stuID" @keyup.enter.native="query" clearable>
        </el-input>
        <el-input class="input-query" placeholder="请输入学生姓名" prefix-icon="el-icon-search"
                  v-model="toolbar.stuName" @keyup.enter.native="query" clearable>
        </el-input>
        <el-input class="input-query" placeholder="请输入院系" prefix-icon="el-icon-search"
                  v-model="toolbar.department" @keyup.enter.native="query" clearable>
        </el-input>
        <el-button class="query-button" type="info" @click="query">查找</el-button>
      </div>
      <el-table class="table" :data="slicedData" v-loading="tableLoading" @sort-change="changeSortType"
                :default-sort="{prop: 'stuID', order: 'ascending'}">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="stuID" label="学号" width="150" :sortable="'custom'"></el-table-column>
        <el-table-column prop="stuName" label="姓名" width="150" :sortable="'custom'"></el-table-column>
        <el-table-column prop="department" label="院系" width="180" :sortable="'custom'"></el-table-column>
        <el-table-column prop="cellphone" label="手机" width="200" :sortable="'custom'"></el-table-column>
        <el-table-column prop="email" label="邮箱" :sortable="'custom'"></el-table-column>
        <el-table-column prop="freeze" label="冻结日期" width="150" :sortable="'custom'">
          <template slot-scope="scope">
            <span v-if="scope.row.freezeStatus">{{ scope.row.freezeDate }}</span>
            <span v-else>未冻结</span>
          </template>
        </el-table-column>
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
      numOptions: [
        {label: '查看近20条', value: 20},
        {label: '查看近50条', value: 50},
        {label: '查看近100条', value: 100},
        {label: '查看近500条', value: 500}
      ],
      toolbar: {
        showNums: 20,
        stuID: '',
        stuName: '',
        department: ''
      },
      tableLoading: false,
      stuList: [
        /*
        {
          userID: '',
          stuID: '202020202',
          stuName: '水神',
          department: '摸鱼学院',
          email: 'happy@my.world',
          cellphone: '12345678900',
          freezeDate: '1970-01-01',
          freezeStatus: true,
        }
        */
      ],
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
  mounted() {
    this.getStuList()
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
      this.tableLoading = true
      let params = {
        limitNum: this.toolbar.showNums
      }
      this.toolbar.stuID && (params.stuID = this.toolbar.stuID)
      this.toolbar.stuName && (params.stuName = this.toolbar.stuName)
      this.toolbar.department && (params.department = this.toolbar.department)
      this.$api.user.queryUserInfo(params).then((res) => {
        if (res.data.errCode === 0) {
          this.stuList = res.data.stuList
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
      this.getStuList()
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

  .choose-num {
    flex-basis: 160px;
  }

  .input-query {
    flex-basis: 200px;
  }

  * + .input-query {
    margin-left: 10px;
  }

  .query-button {
    margin-left: 10px;
  }
}

.pagination {
  margin-top: $--pagination-margin-top;
  margin-bottom: $--pagination-margin-bottom;
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
  color: orangered;

  &:focus, &:hover {
    color: mix(orangered, $--color-white, 75%);
  }

  &:active {
    color: mix(orangered, $--color-black, 75%);
  }
}

</style>