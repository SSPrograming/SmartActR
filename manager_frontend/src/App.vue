<template>
  <div id="app">
    <h1><img class="logo" src="./assets/logo.png" alt="Logo"/>智慧活动室</h1>
    <el-divider></el-divider>
    <div class="container">
      <transition name="sidebar">
        <aside v-if="!isLogin">
          <Sidebar></Sidebar>
        </aside>
      </transition>
      <main class="main">
        <transition name="router-view">
          <router-view></router-view>
        </transition>
      </main>
    </div>
  </div>
</template>

<script>
import Sidebar from "./components/Sidebar";

export default {
  components: {
    Sidebar
  },
  computed: {
    isLogin() {
      return this.$route.name === 'Login'
    }
  },
  mounted() {
    // 在卸载前删除本地存储的登陆状态
    window.addEventListener('beforeunload', () => {
      localStorage.removeItem('jwt')
    })
  }
}
</script>

<style lang="scss">
#app {
  width: 90%;
  margin: 0 auto;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

h1 {
  display: flex;
  padding-left: 10px;
  font-family: '微软雅黑', sans-serif;
  color: hotpink;
  line-height: 50px;
  cursor: default;
}

.logo {
  width: 50px;
  margin-right: 15px;
}

.container {
  display: flex;
  margin: 0 auto;
}

aside {
  width: 240px;
}

main {
  flex: 1;
  padding: 20px;
}

.sidebar-enter-active, .sidebar-leave-active {
  transition: all .5s ease-in-out;
}

.sidebar-enter, .sidebar-leave-to {
  margin-left: -240px;
  opacity: 0;
}

.router-view-enter-active, .router-view-leave-active {
  transition: all .5s ease-in-out;
}

.router-view-enter, .router-view-leave-to {
  height: 0;
  opacity: 0;
}

</style>
