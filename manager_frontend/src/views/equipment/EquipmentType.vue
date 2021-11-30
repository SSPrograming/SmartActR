<template>
  <div class="equipment-type">
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
            <el-button class="button" type="text">编辑</el-button>
            <el-button class="button delete" type="text">删除</el-button>
            <el-button class="button lookup" type="text">查看详情</el-button>
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
              <img :src="'http://' + item.equipmentImage" class="equipment-image" alt="">
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import Toolbar from '@/components/Toolbar'

export default {
  name: "EquipmentType",
  components: {
    Toolbar
  },
  data() {
    return {
      loading: false,
      equipmentTypeList: [],
      form: {
        equipmentName: '',
        equipmentCount: 0,
        equipmentDescription: '',
        equipmentImage: ''
      }
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