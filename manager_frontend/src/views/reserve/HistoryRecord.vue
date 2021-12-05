<template>
  <div class="history-record">
    <div class="container">
      <ReserveView :record-info="recordInfo" show-equipment-name show-user-name
                   @refresh="getRecordList" @query="query"></ReserveView>
    </div>
  </div>
</template>

<script>
import ReserveView from '@/components/ReserveView'

export default {
  name: "TodayRecord",
  components: {
    ReserveView
  },
  data() {
    return {
      recordInfo: {
        toolbar: {
          queryStartDate: null,
          queryEndDate: null
        },
        tableLoading: false,
        recordList: [
          /*
          {
            recordID: 0,
            postTime: '',
            reserveDate: '',
            startTime: '',
            endTime: '',
            username: '',
            status: '',
            equipmentName: ''
          }
          */
        ]
      }
    }
  },
  mounted() {
    this.recordInfo.toolbar.queryStartDate = new Date()
    this.recordInfo.toolbar.queryStartDate.setDate(this.recordInfo.toolbar.queryStartDate.getDate() - 8)
    this.recordInfo.toolbar.queryEndDate = new Date()
    this.recordInfo.toolbar.queryEndDate.setDate(this.recordInfo.toolbar.queryEndDate.getDate() - 1)
    this.getRecordList()
  },
  methods: {
    getRecordList() {
      if (!this.recordInfo.toolbar.queryStartDate || !this.recordInfo.toolbar.queryEndDate ||
          this.recordInfo.toolbar.queryStartDate > this.recordInfo.toolbar.queryEndDate) {
        this.$utils.alertMessage(this, '请选择正确的时间区间', 'warning')
        return
      }
      const params = {
        startDate: this.recordInfo.toolbar.queryStartDate && this.$utils.time.format(this.recordInfo.toolbar.queryStartDate, 'yyyy-MM-dd'),
        endDate: this.recordInfo.toolbar.queryEndDate && this.$utils.time.format(this.recordInfo.toolbar.queryEndDate, 'yyyy-MM-dd')
      }
      this.recordInfo.tableLoading = true
      this.$api.reserve.getHistoryRecord(params).then((res) => {
        if (res.data.errCode === 0) {
          this.recordInfo.recordList = res.data.recordList
          this.$utils.alertMessage(this, '获取数据成功', 'success')
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.recordInfo.tableLoading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.recordInfo.tableLoading = false
      })
    },
    query() {
      if (this.recordInfo.toolbar.queryStartDate && this.recordInfo.toolbar.queryEndDate) {
        this.getRecordList()
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

.pagination {
  margin-top: $--pagination-margin-top;
}
</style>
