<template>
  <div class="equipment-detail">
    <el-dialog title="设备二维码" :visible.sync="showQRCode" v-loading="dialogLoading" @closed="clearQRCode">
      <div style="text-align: right;">
        <el-button type="primary" plain @click="handleRefresh">重新生成</el-button>
      </div>
      <div style="text-align: center;">
        <el-image class="qrcode" :src="qrcodeURL"></el-image>
      </div>
      <div style="text-align: center; margin-top: 10px;">
        <el-button class="button" type="info" plain @click="showQRCode=false">取消</el-button>
        <el-button class="button" type="primary" plain @click="showQRCode=false">确认</el-button>
      </div>
    </el-dialog>
    <el-dialog title="设备编辑" :visible.sync="showEquipmentEditor" v-loading="dialogLoading">
      <EquipmentEditor :form="form" @editorCancel="editorCancel" @editorConfirm="editorConfirm"></EquipmentEditor>
    </el-dialog>
    <el-dialog title="预约记录" :visible.sync="showReserveRecord" v-loading="dialogLoading" width="80%">
      <ReserveView :record-info="recordInfo" @refresh="getRecordList" @query="query"
                   @hide="showReserveRecord=false" show-user-name dialog></ReserveView>
    </el-dialog>
    <div class="container">
      <div class="header">
        <Toolbar back refresh @back="$router.push({name: 'EquipmentType'})" @refresh="getEquipmentList"></Toolbar>
        <el-button type="primary" plain @click="handleAdd">添加设备</el-button>
      </div>
      <el-table class="table" :data="slicedData" v-loading="tableLoading" @sort-change="changeSortType"
                :default-sort="{prop: 'equipmentID', order: 'ascending'}">
        <el-table-column prop="equipmentID" label="设备编号" width="150px" :sortable="'custom'"></el-table-column>
        <el-table-column prop="equipmentName" label="设备名称" width="250px" :sortable="'custom'"></el-table-column>
        <el-table-column prop="equipmentStatus" label="设备状态" :sortable="'custom'"></el-table-column>
        <el-table-column fixed="right" label="操作" width="200">
          <template slot-scope="scope">
            <div class="operation">
              <el-button type="text" size="small" @click="handleEdit(scope.row)">编辑</el-button>
              <el-button type="text" size="small" class="delete" @click="handleDelete(scope.row)">删除</el-button>
              <el-button type="text" size="small" class="lookup" @click="handleLookUp(scope.row)">预约记录</el-button>
              <img class="icon-qrcode pointer" src="../../assets/qrcode.png" alt="qrcode"
                   @click="handleShowQRCode(scope.row)"/>
            </div>
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
import Toolbar from '@/components/Toolbar'
import EquipmentEditor from '@/components/Editor/EquipmentEditor'
import ReserveView from '@/components/ReserveView'

export default {
  name: "EquipmentDetail",
  components: {
    EquipmentEditor,
    Toolbar,
    ReserveView
  },
  data() {
    return {
      equipmentType: 0,
      tableLoading: false,
      equipmentList: [],
      sortType: {
        prop: 'equipmentID',
        order: 'ascending'
      },
      pageSize: 5,
      currentPage: 1,
      dialogLoading: false,
      showEquipmentEditor: false,
      form: {
        equipmentName: '',
        equipmentID: 0,
        equipmentStatus: '',
      },
      showReserveRecord: false,
      recordInfo: {
        toolbar: {
          queryStartDate: null,
          queryEndDate: null
        },
        tableLoading: false,
        recordList: [],
        equipmentID: 0
      },
      showQRCode: false,
      qrcodeURL: '',
      qrcodeRef: {
        /*
        equipmentType: this.equipmentType,
        equipmentID: row.equipmentID
        */
      }
    }
  },
  computed: {
    dataLength() {
      return this.equipmentList.length
    },
    slicedData() {
      this.doSort()
      return this.equipmentList.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage <= this.equipmentList.length ?
              this.pageSize * this.currentPage : this.equipmentList.length)
    }
  },
  mounted() {
    if (this.$route.query.equipmentType) {
      this.equipmentType = Number.parseInt(this.$route.query.equipmentType)
      this.getEquipmentList()
      this.recordInfo.toolbar.queryStartDate = new Date()
      this.recordInfo.toolbar.queryStartDate.setDate(this.recordInfo.toolbar.queryStartDate.getDate() - 8)
      this.recordInfo.toolbar.queryEndDate = new Date()
      this.recordInfo.toolbar.queryEndDate.setDate(this.recordInfo.toolbar.queryEndDate.getDate() + 8)
    } else {
      this.$router.push({name: 'EquipmentType'})
    }
  },
  methods: {
    changeSortType(event) {
      if (event) {
        this.sortType.prop = event.prop
        this.sortType.order = event.order
      }
      if (!this.sortType.order) {
        this.sortType.prop = 'equipmentID'
        this.sortType.order = 'ascending'
      }
    },
    doSort() {
      this.$utils.sort(this.equipmentList, this.sortType, 'equipmentID')
    },
    getEquipmentList() {
      this.tableLoading = true
      this.$api.equipment.getAllEquipment({equipmentType: this.equipmentType}).then((res) => {
        if (res.data.errCode === 0) {
          this.equipmentList = res.data.equipmentList
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
    getRecordList() {
      if (this.recordInfo.toolbar.queryStartDate && this.recordInfo.toolbar.queryEndDate &&
          this.recordInfo.toolbar.queryStartDate > this.recordInfo.toolbar.queryEndDate) {
        this.$utils.alertMessage(this, '请选择正确的时间区间', 'warning')
        return
      }
      const params = {
        equipmentType: this.equipmentType,
        equipmentID: this.recordInfo.equipmentID,
        startDate: this.recordInfo.toolbar.queryStartDate && this.$utils.time.format(this.recordInfo.toolbar.queryStartDate, 'yyyy-MM-dd'),
        endDate: this.recordInfo.toolbar.queryEndDate && this.$utils.time.format(this.recordInfo.toolbar.queryEndDate, 'yyyy-MM-dd')
      }
      this.recordInfo.tableLoading = true
      this.$api.equipment.getEquipmentRecordList(params).then((res) => {
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
      this.getRecordList()
    },
    handleAdd() {
      this.$confirm('此操作将添加一台该类设备, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        this.tableLoading = true
        this.$api.equipment.addEquipment({equipmentType: this.equipmentType}).then((res) => {
          if (res.data.errCode === 0) {
            this.getEquipmentList()
            this.$utils.alertMessage(this, '添加成功', 'success')
          } else {
            this.$utils.error.APIError(this, res.data)
            this.tableLoading = false
          }
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.tableLoading = false
        })
      }).catch(() => {
      })
    },
    handleEdit(row) {
      this.form = {...row}
      this.showEquipmentEditor = true
    },
    handleDelete(row) {
      this.$confirm('此操作将删除该台设备, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const params = {
          equipmentType: this.equipmentType,
          equipmentID: row.equipmentID
        }
        this.tableLoading = true
        this.$api.equipment.deleteEquipment(params).then((res) => {
          if (res.data.errCode === 0) {
            this.getEquipmentList()
            this.$utils.alertMessage(this, '删除成功', 'success')
          } else {
            this.$utils.error.APIError(this, res.data)
            this.tableLoading = false
          }
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.tableLoading = false
        })
      }).catch(() => {
      })
    },
    handleLookUp(row) {
      this.recordInfo.equipmentID = row.equipmentID
      this.getRecordList()
      this.showReserveRecord = true
    },
    editorCancel() {
      this.showEquipmentEditor = false
    },
    editorConfirm() {
      this.dialogLoading = true
      const params = {
        equipmentType: this.equipmentType,
        equipmentID: this.form.equipmentID,
        equipmentStatus: this.form.equipmentStatus
      }
      this.dialogLoading = true
      this.$api.equipment.editEquipment(params).then((res) => {
        if (res.data.errCode === 0) {
          this.getEquipmentList()
          this.$utils.alertMessage(this, '编辑成功', 'success')
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.dialogLoading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.dialogLoading = false
      })
      this.showEquipmentEditor = false
    },
    handleShowQRCode(row) {
      this.showQRCode = true
      this.dialogLoading = true
      this.qrcodeRef = {
        equipmentType: this.equipmentType,
        equipmentID: row.equipmentID
      }
      this.$api.qrcode.getQRCode(this.qrcodeRef).then((res) => {
        if (res.data.errCode === 0) {
          this.qrcodeURL = res.data.qrcodeURL + '?time=' + new Date().getTime()
          this.$utils.alertMessage(this, '获取二维码成功', 'success')
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.dialogLoading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.dialogLoading = false
      })
    },
    handleRefresh() {
      this.dialogLoading = true
      this.$api.qrcode.refreshQRCode(this.qrcodeRef).then((res) => {
        if (res.data.errCode === 0) {
          this.qrcodeURL = res.data.qrcodeURL + '?time=' + new Date().getTime()
          this.$utils.alertMessage(this, '获取二维码成功', 'success')
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.dialogLoading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.dialogLoading = false
      })
    },
    clearQRCode() {
      this.qrcodeURL = ''
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

.operation {
  display: flex;
  align-items: center;

  .delete {
    color: $--color-danger;

    &:focus, &:hover {
      color: mix($--color-danger, $--color-white, 75%);
    }

    &:active {
      color: mix($--color-danger, $--color-black, 75%);
    }
  }

  .lookup {
    color: $--color-lookup;

    &:focus, &:hover {
      color: mix($--color-lookup, $--color-white, 75%);
    }

    &:active {
      color: mix($--color-lookup, $--color-black, 75%);
    }
  }

  .icon-qrcode {
    width: 18px;
    height: 18px;
    margin-left: 10px;
  }
}

.qrcode {
  width: 298px;
  height: 298px;
  border: 1px dashed #d9d9d9;
}

</style>
