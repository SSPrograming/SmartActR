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
    <div class="container">
      <div class="header">
        <Toolbar back refresh @back="$router.push({name: 'EquipmentType'})" @refresh="getEquipmentList"></Toolbar>
        <el-button type="primary" plain @click="handleAdd">添加设备</el-button>
      </div>
    </div>
    <el-table class="table" :data="slicedData" v-loading="tableLoading" @sort-change="doSort"
              :default-sort="{prop: 'equipmentID', order: 'ascending'}">
      <el-table-column prop="equipmentID" label="设备编号" width="150px" :sortable="'custom'"></el-table-column>
      <el-table-column prop="equipmentName" label="设备名称" width="250px" :sortable="'custom'"></el-table-column>
      <el-table-column prop="equipmentStatus" label="设备状态" :sortable="'custom'">
        <template slot-scope="scope">
          <span>{{ status2string(scope.row.equipmentStatus) }}</span>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="150">
        <template slot-scope="scope">
          <div class="operation">
            <el-button type="text" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" size="small" class="delete" @click="handleDelete(scope.row)">删除</el-button>
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
</template>

<script>
import Toolbar from '@/components/Toolbar'
import EquipmentEditor from '@/components/Editor/EquipmentEditor'

export default {
  name: "EquipmentDetail",
  components: {
    EquipmentEditor,
    Toolbar
  },
  data() {
    return {
      dialogLoading: false,
      showQRCode: false,
      qrcodeURL: '',
      qrcodeRef: {},
      tableLoading: false,
      equipmentType: 0,
      equipmentList: [
        {
          equipmentID: 1,
          equipmentName: '3D打印机',
          equipmentStatus: 0,
        },
        {
          equipmentID: 2,
          equipmentName: '3D打印机',
          equipmentStatus: 0,
        }
      ],
      sortType: {
        prop: 'equipmentID',
        order: 'ascending'
      },
      pageSize: 10,
      currentPage: 1,
      showEquipmentEditor: false,
      form: {
        equipmentName: '',
        equipmentID: 0,
        equipmentStatus: 0,
      }
    }
  },
  computed: {
    dataLength() {
      return this.equipmentList.length
    },
    slicedData() {
      return this.equipmentList.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage <= this.equipmentList.length ?
              this.pageSize * this.currentPage : this.equipmentList.length)
    }
  },
  mounted() {
    this.equipmentType = this.$route.query.equipmentType
    this.getEquipmentList()
  },
  methods: {
    doSort(event) {
      if (event) {
        this.sortType.prop = event.prop
        this.sortType.order = event.order
      }
      if (!this.sortType.order) {
        this.sortType.prop = 'noticeID'
        this.sortType.order = 'descending'
      }
      this.$utils.sort(this.equipmentList, this.sortType, 'equipmentID')
    },
    status2string(status) {
      return this.$api.equipment.status2string[status]
    },
    getEquipmentList() {

    },
    handleAdd() {
      this.$confirm('此操作将添加一台该类设备, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {

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
        console.log(row)
      }).catch(() => {
      })
    },
    editorCancel() {
      this.showEquipmentEditor = false
    },
    editorConfirm() {
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

.qrcode {
  width: 298px;
  height: 298px;
  border: 1px dashed #d9d9d9;
}

.pagination {
  margin-top: $--pagination-margin-top;
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

  .icon-qrcode {
    width: 18px;
    height: 18px;
    margin-left: 10px;
  }
}

</style>
