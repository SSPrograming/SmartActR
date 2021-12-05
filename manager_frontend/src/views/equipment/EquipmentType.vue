<template>
  <div class="equipment-type">
    <el-dialog title="设备种类编辑" :visible.sync="showEquipmentTypeEditor" v-loading="dialogLoading">
      <EquipmentTypeEditor :form="form" :add="editEquipmentType === null"
                           @editorConfirm="editorConfirm" @editorCancel="editorCancel">
      </EquipmentTypeEditor>
    </el-dialog>
    <div class="container">
      <div class="header">
        <Toolbar refresh @refresh="getAllEquipmentType"></Toolbar>
        <el-button type="primary" plain @click="handleAdd">添加设备种类</el-button>
      </div>
      <div class="main" v-loading="loading">
        <el-card class="card" v-for="(item, index) in equipmentTypeList" :key="item.equipmentType">
          <div slot="header" class="card-header">
            <span>{{ item.equipmentName }}</span>
            <span class="whitespace"></span>
            <el-button class="button move" type="text" @click="handleMoveUp(index)" :disabled="index===0">上移</el-button>
            <el-button class="button move" type="text" @click="handleMoveDown(index)"
                       :disabled="index===equipmentTypeList.length - 1">下移
            </el-button>
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
              <img :src="toDynamicImageUrl(item.equipmentImage)" class="equipment-image" alt=""/>
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
      dialogLoading: false,
      showEquipmentTypeEditor: false,
      editEquipmentType: null,
      form: {
        equipmentName: '',
        equipmentCount: 1,
        equipmentDescription: '',
        equipmentImage: null,
      }
    }
  },
  mounted() {
    this.getAllEquipmentType()
  },
  methods: {
    toDynamicImageUrl(imageUrl) {
      return imageUrl /* + '?time=' + new Date().getTime() */
    },
    getAllEquipmentType() {
      this.loading = true
      this.$api.equipment.getAllEquipmentType().then((res) => {
        if (res.data.errCode === 0) {
          this.equipmentTypeList = res.data.TypeList
          const sortType = {
            prop: 'equipmentOrder',
            order: 'ascending'
          }
          this.$utils.sort(this.equipmentTypeList, sortType, 'equipmentType')
          this.$utils.alertMessage(this, '获取数据成功', 'success')
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
      this.showEquipmentTypeEditor = true
    },
    handleMoveUp(index) {
      const curr = this.equipmentTypeList[index]
      const prev = this.equipmentTypeList[index - 1]
      const params = {
        equipmentType1: curr.equipmentType,
        equipmentType2: prev.equipmentType
      }
      this.loading = true
      this.$api.equipment.swapEquipmentOrder(params).then((res) => {
        if (res.data.errCode === 0) {
          this.$utils.alertMessage(this, '上移成功', 'success')
          this.getAllEquipmentType()
        } else {
          this.$utils.error.APIError(this, res.data)
          this.loading = false
        }
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.loading = false
      })
    },
    handleMoveDown(index) {
      const curr = this.equipmentTypeList[index]
      const next = this.equipmentTypeList[index + 1]
      const params = {
        equipmentType1: curr.equipmentType,
        equipmentType2: next.equipmentType
      }
      this.loading = true
      this.$api.equipment.swapEquipmentOrder(params).then((res) => {
        if (res.data.errCode === 0) {
          this.$utils.alertMessage(this, '上移成功', 'success')
          this.getAllEquipmentType()
        } else {
          this.$utils.error.APIError(this, res.data)
          this.loading = false
        }
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.loading = false
      })
    },
    handleEdit(item) {
      this.editEquipmentType = item.equipmentType
      this.form = {
        equipmentName: item.equipmentName,
        equipmentCount: item.equipmentCount,
        equipmentDescription: item.equipmentDescription,
        equipmentImage: item.equipmentImage,
      }
      this.showEquipmentTypeEditor = true
    },
    handleDelete(item) {
      this.$confirm('此操作将删除该类设备, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        setTimeout(() => {
          this.$confirm('这将影响到所有的该类设备，是否继续？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.loading = true
            this.$api.equipment.deleteEquipmentType({equipmentType: item.equipmentType}).then((res) => {
              if (res.data.errCode === 0) {
                this.$utils.alertMessage(this, '删除成功', 'success')
                this.getAllEquipmentType()
              } else {
                this.$utils.error.APIError(this, res.data)
                this.loading = false
              }
            }).catch((err) => {
              this.$utils.error.ServerError(this, err)
              this.loading = false
            })
          }).catch(() => {
          })
        }, 500)
      }).catch(() => {
      })
    },
    handleDetail(item) {
      this.$router.push({
        name: 'EquipmentDetail',
        query: {
          equipmentType: item.equipmentType
        }
      })
    },
    editorCancel() {
      this.showEquipmentTypeEditor = false
    },
    editorConfirm() {
      this.dialogLoading = true
      // 创建
      if (!this.editEquipmentType) {
        let formData = new FormData()
        formData.append('equipmentName', this.form.equipmentName)
        formData.append('equipmentCount', this.form.equipmentCount)
        formData.append('equipmentDescription', this.form.equipmentDescription)
        formData.append('equipmentImage', this.form.equipmentImage)
        this.$api.equipment.addEquipmentType(formData).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '添加成功', 'success')
            this.form = {
              equipmentName: '',
              equipmentCount: 1,
              equipmentDescription: '',
              equipmentImage: null,
            }
            this.getAllEquipmentType()
          } else {
            this.$utils.error.APIError(this, res.data)
          }
          this.dialogLoading = false
          this.showEquipmentTypeEditor = false
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.dialogLoading = false
          this.showEquipmentTypeEditor = false
        })
      }
      // 编辑
      else {
        let formData = new FormData()
        formData.append('equipmentType', this.editEquipmentType)
        formData.append('equipmentName', this.form.equipmentName)
        formData.append('equipmentDescription', this.form.equipmentDescription)
        if (typeof this.form.equipmentImage === "object") {
          formData.append('equipmentImage', this.form.equipmentImage)
        }
        this.$api.equipment.editEquipmentType(formData).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '编辑成功', 'success')
            this.getAllEquipmentType()
          } else {
            this.$utils.error.APIError(this, res.data)
          }
          this.dialogLoading = false
          this.showEquipmentTypeEditor = false
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.dialogLoading = false
          this.showEquipmentTypeEditor = false
        })
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

.main {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-around;
  padding-top: 20px;

  .card {
    flex-basis: 650px;
    margin-bottom: 30px;
  }
}

.card-header {
  display: flex;
  align-items: center;

  .button {
    padding: 3px 0;
  }

  .move {
    color: $--color-move;

    &:focus, &:hover {
      color: mix($--color-move, $--color-white, 75%);
    }

    &:active {
      color: mix($--color-move, $--color-black, 75%);
    }

    &[disabled] {
      color: #c0c4cc;
    }
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
      display: block;
      width: 100%;
      max-height: 356px;
    }
  }
}

.whitespace {
  flex: 1;
}
</style>
