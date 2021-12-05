<template>
  <div class="reserve-view">
    <div class="header">
      <Toolbar :toolbar="recordInfo.toolbar" choose-date refresh @refresh="$emit('refresh')"
               @query="$emit('query')"></Toolbar>
    </div>
    <el-table class="table" :data="slicedData" v-loading="recordInfo.tableLoading" @sort-change="changeSortType"
              :default-sort="{prop: 'recordID', order: 'descending'}">
      <el-table-column type="index" width="50"></el-table-column>
      <el-table-column prop="reserveDate" label="预约日期" :sortable="'custom'"></el-table-column>
      <el-table-column prop="startTime" label="开始时间" :sortable="'custom'"></el-table-column>
      <el-table-column prop="endTime" label="结束时间" :sortable="'custom'"></el-table-column>
      <el-table-column prop="equipmentName" label="设备名称" :sortable="'custom'"
                       v-if="showEquipmentName"></el-table-column>
      <el-table-column prop="userName" label="预约人" :sortable="'custom'" v-if="showUserName"></el-table-column>
      <el-table-column prop="postTime" label="提交时间" :sortable="'custom'"></el-table-column>
      <el-table-column prop="status" label="预约状态" :sortable="'custom'"></el-table-column>
    </el-table>
    <el-pagination class="pagination" layout="prev, pager, next" :page-size="pageSize"
                   :current-page.sync="currentPage" :total="dataLength" background>
    </el-pagination>
    <div style="text-align: center; margin-top: 10px;" v-if="dialog">
      <el-button class="button" type="info" plain @click="$emit('hide')">取消</el-button>
      <el-button class="button" type="primary" plain @click="$emit('hide')">确认</el-button>
    </div>
  </div>
</template>

<script>
import Toolbar from '@/components/Toolbar'

export default {
  name: "ReserveView",
  components: {
    Toolbar
  },
  props: {
    recordInfo: {
      toolbar: {
        queryStartDate: Date,
        queryEndDate: Date
      },
      tableLoading: Boolean,
      recordList: Array
    },
    showEquipmentName: Boolean,
    showUserName: Boolean,
    dialog: Boolean,
  },
  data() {
    return {
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
      return this.recordInfo.recordList.length
    },
    slicedData() {
      this.doSort()
      return this.recordInfo.recordList.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage <= this.recordInfo.recordList.length ?
              this.pageSize * this.currentPage : this.recordInfo.recordList.length)
    }
  },
  methods: {
    changeSortType(event) {
      if (event) {
        this.sortType.prop = event.prop
        this.sortType.order = event.order
      }
      if (!this.sortType.order) {
        this.sortType.prop = 'recordID'
        this.sortType.order = 'descending'
      }
    },
    doSort() {
      this.$utils.sort(this.recordInfo.recordList, this.sortType, 'recordID')
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
  margin-bottom: $--pagination-margin-bottom;
}

</style>
