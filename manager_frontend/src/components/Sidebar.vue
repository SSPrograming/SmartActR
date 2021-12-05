<template>
  <div class="sidebar">
    <el-menu :default-active="routeName" @select="handleSelect">
      <!-- 首页 -->
      <el-menu-item index="Home">
        <template slot="title">
          <i class="el-icon-s-home"></i>
          <span>首页</span>
        </template>
      </el-menu-item>
      <!-- 公告管理 -->
      <el-menu-item index="Notice">
        <template slot="title">
          <i class="el-icon-document"></i>
          <span>公告管理</span>
        </template>
      </el-menu-item>
      <!-- 预约管理 -->
      <el-submenu index="Reserve">
        <template slot="title">
          <i class="el-icon-date"></i>
          <span>预约管理</span>
        </template>
        <el-menu-item index="TodayRecord">
          <template slot="title">
            <span>今日预约</span>
          </template>
        </el-menu-item>
        <el-menu-item index="HistoryRecord">
          <template slot="title">
            <span>历史预约</span>
          </template>
        </el-menu-item>
      </el-submenu>
      <!-- 设备管理 -->
      <el-submenu index="Equipment">
        <template slot="title">
          <i class="el-icon-setting"></i>
          <span>设备管理</span>
        </template>
        <el-menu-item index="EquipmentType">
          <template slot="title">
            <span>设备详情</span>
          </template>
        </el-menu-item>
        <el-menu-item index="EquipmentRules">
          <template slot="title">
            <span>独占规则</span>
          </template>
        </el-menu-item>
      </el-submenu>
      <!-- 使用说明 -->
      <el-menu-item index="Instruction">
        <template slot="title">
          <i class="el-icon-collection"></i>
          <span>使用说明</span>
        </template>
      </el-menu-item>
      <!-- 用户管理 -->
      <el-submenu index="User">
        <template slot="title">
          <i class="el-icon-user"></i>
          <span>用户管理</span>
        </template>
        <el-menu-item index="User">
          <template slot="title">
            <span>用户信息</span>
          </template>
        </el-menu-item>
        <el-menu-item index="FeedBack">
          <template slot="title">
            <span>反馈消息</span>
          </template>
        </el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "Sidebar",
  computed: {
    routeName() {
      return this.$route.name === 'EquipmentDetail' ? 'EquipmentType'
          : this.$route.name === 'InstructionEditor' ? 'Instruction'
              : this.$route.name
    }
  },
  methods: {
    handleSelect(index) {
      if (this.$route.name !== index) {
        this.$router.push({
          name: index
        })
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>
