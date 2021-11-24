<template>
  <div class="sidebar">
    <el-menu
        default-active="this.show"
        class="el-menu-vertical-demo"
        @select="handleSelect"
    >
      <el-menu-item index="Home">
        <i class="el-icon-s-home"></i>
        <span slot="title">首页</span>
      </el-menu-item>
      <el-menu-item index="Notice">
        <i class="el-icon-document"></i>
        <span slot="title">公告</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "Sidebar",
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

<style scoped>
.sidebar {
  min-width: 160px;
}
</style>