<template>
  <div class="today-record">
    <div class="container">
      <div class="header">
        <Toolbar refresh @refresh="getRecordList"></Toolbar>
      </div>
      <el-table class="table" :data="slicedData" v-loading="tableLoading" @sort-change="doSort"
                :default-sort="{prop: 'recordID', order: 'descending'}">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="reserveDate" label="预约日期" :sortable="'custom'"></el-table-column>
        <el-table-column prop="startTime" label="开始时间" :sortable="'custom'"></el-table-column>
        <el-table-column prop="endTime" label="结束时间" :sortable="'custom'"></el-table-column>
        <el-table-column prop="equipmentName" label="设备名称" :sortable="'custom'"></el-table-column>
        <el-table-column prop="userName" label="预约人" :sortable="'custom'"></el-table-column>
        <el-table-column prop="postTime" label="提交时间" :sortable="'custom'"></el-table-column>
        <el-table-column prop="status" label="预约状态" :sortable="'custom'"></el-table-column>
      </el-table>
      <el-pagination class="pagination" layout="prev, pager, next" :page-size="pageSize"
                     :current-page.sync="currentPage" :total="dataLength" background>
      </el-pagination>
    </div>
  </div>
</template>

<script>
import Toolbar from '@/components/Toolbar'

export default {
  name: "TodayRecord",
  components: {
    Toolbar
  },
  data() {
    return {
      tableLoading: false,
      recordList: [{
        recordID: 0,
        postTime: '',
        reserveDate: '',
        startTime: '',
        endTime: '',
        username: '',
        status: '',
        equipmentName: ''
      }],
      sortType: {
        prop: 'recordID',
        order: 'descending'
      },
      pageSize: 10,
      currentPage: 1
    }
  },
  computed: {
    dataLength() {
      return this.recordList.length
    },
    slicedData() {
      return this.recordList.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage <= this.recordList.length ?
              this.pageSize * this.currentPage : this.recordList.length)
    }
  },
  mounted() {
    this.getRecordList()
  },
  methods: {
    doSort(event) {
      if (event) {
        this.sortType.prop = event.prop
        this.sortType.order = event.order
      }
      if (!this.sortType.order) {
        this.sortType.prop = 'recordID'
        this.sortType.order = 'descending'
      }
      this.$utils.sort(this.recordList, this.sortType, 'recordID')
    },
    getRecordList() {
      this.tableLoading = true
      this.$api.reserve.getTodayRecord().then((res) => {
        if (res.data.errCode === 0) {
          this.recordList = res.data.recordList
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

.pagination {
  margin-top: $--pagination-margin-top;
}
</style>
