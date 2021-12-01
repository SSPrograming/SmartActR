<template>
  <div class="equipment-type">
    <el-dialog title="设备种类编辑" :visible.sync="showEquipmentEditor" v-loading="dialogLoading">
      <EquipmentTypeEditor :form="form" @editorCancel="editorCancel"
                           @editorConfirm="editorConfirm" :add="editEquipmentType === null"></EquipmentTypeEditor>
    </el-dialog>
    <div class="container">
      <div class="header">
        <Toolbar refresh @refresh="getAllEquipmentType"></Toolbar>
        <el-button type="primary" plain @click="handleAdd">添加设备</el-button>
      </div>
      <div class="main" v-loading="loading">
        <el-card class="card" v-for="item in equipmentTypeList" :key="item.equipmentType">
          <div slot="header" class="card-header">
            <span>{{ item.equipmentName }}</span>
            <span class="whitespace"></span>
            <el-button class="button" type="text" @click="handleEdit(item)">编辑</el-button>
            <el-button class="button delete" type="text" @click="handleDelete(item)">删除</el-button>
            <el-button class="button lookup" type="text" @click="handleDetail(item)">查看详情</el-button>
          </div>
          <div class="equipment-content">
            <div class="left">
              <div class="equipment-count">
                <div class="label"> 设备数量：</div>
                <div class="content">
                  {{ item.equipmentCount }}
                </div>
              </div>
              <div class="equipment-description">
                <div class="label">设备描述：</div>
                <div class="content">
                  {{ item.equipmentDescription }}
                </div>
              </div>
            </div>
            <div class="right">
              <img :src="item.equipmentImage" class="equipment-image" alt="">
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import Toolbar from '@/components/Toolbar'
import EquipmentTypeEditor from '@/components/Editor/EquipmentTypeEditor'

export default {
  name: "EquipmentType",
  components: {
    EquipmentTypeEditor,
    Toolbar
  },
  data() {
    return {
      loading: false,
      equipmentTypeList: [],
      form: {
        equipmentName: '',
        equipmentCount: 1,
        equipmentDescription: '',
        equipmentImage: null,
      },
      editEquipmentType: null,
      dialogLoading: false,
      showEquipmentEditor: false
    }
  },
  mounted() {
    this.getAllEquipmentType()
  },
  methods: {
    getAllEquipmentType() {
      this.loading = true
      this.$api.equipment.getAllEquipmentType().then((res) => {
        if (res.data.errCode === 0) {
          this.equipmentTypeList = res.data.TypeList
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.loading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.loading = false
      })
    },
    handleAdd() {
      if (this.editEquipmentType) {
        this.editEquipmentType = null
        this.form = {
          equipmentName: '',
          equipmentCount: 1,
          equipmentDescription: '',
          equipmentImage: null,
        }
      }
      this.showEquipmentEditor = true
    },
    handleEdit(item) {
      this.editEquipmentType = item.equipmentType
      this.form = {
        equipmentName: item.equipmentName,
        equipmentCount: item.equipmentCount,
        equipmentDescription: item.equipmentDescription,
        equipmentImage: item.equipmentImage,
      }
      this.showEquipmentEditor = true
    },
    handleDelete(item) {
      this.$confirm('此操作将删除该类设备, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        setTimeout(() => {
          this.$confirm('这将影响到所有的预约记录，是否继续？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            console.log(item)
          }).catch(() => {

          })
        }, 500)
      }).catch(() => {
      })
    },
    handleDetail(item) {
      this.$router.push({
        name: 'EquipmentDetail',
        query: item
      })
    },
    editorCancel() {
      this.showEquipmentEditor = false
    },
    editorConfirm() {
      let formData = new FormData()
      formData.append('testFile', this.form.equipmentImage)
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

.main {
  display: flex;
  flex-wrap: wrap;
  padding-top: 20px;

  .card {
    flex-basis: 650px;
    margin: 0 30px 30px;
  }
}

.card-header {
  display: flex;

  .button {
    padding: 3px 0;
  }

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
    color: green;

    &:focus, &:hover {
      color: mix(green, $--color-white, 75%);
    }

    &:active {
      color: mix(green, $--color-black, 75%);
    }
  }
}

.equipment-content {
  display: flex;

  .left {
    flex: 1;
    padding-right: 10px;

    .label {
      flex-basis: 80px;
      line-height: 21px;
    }

    .content {
      flex: 1;
      line-height: 21px;
    }

    .equipment-count, .equipment-description {
      display: flex;
    }

    .equipment-description {
      margin-top: 5px;
    }
  }

  .right {
    flex-basis: 200px;

    .equipment-image {
      width: 100%;
      display: block;
    }
  }
}

.whitespace {
  flex: 1;
}
</style>