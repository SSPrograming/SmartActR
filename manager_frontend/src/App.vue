<template>
  <div id="app">
    <header>
      <h1><img class="logo" src="./assets/logo.png" alt="Logo"/>智慧活动室</h1>
      <el-button type="primary" @click="logout" plain>登出</el-button>
    </header>
    <el-divider></el-divider>
    <div class="container">
      <transition name="sidebar">
        <aside v-if="!isLogin">
          <Sidebar></Sidebar>
        </aside>
      </transition>
      <main class="main">
        <router-view></router-view>
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
  },
  methods: {
    logout() {
      this.$store.commit('logout')
      if (this.$route.name !== 'Login') {
        this.$router.replace({name: 'Login'})
        this.$utils.alertMessage(this, '登出成功', 'success');
      }
    }
  }
}
</script>

<style scoped lang="scss">
@import "src/element-variables";

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h1 {
  display: flex;
  padding-left: 10px;
  font-family: '微软雅黑', sans-serif;
  color: $--color-primary;
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
  padding: 0 20px;
}

.sidebar-enter-active, .sidebar-leave-active {
  transition: all .5s ease-in-out;
}

.sidebar-enter, .sidebar-leave-to {
  margin-left: -240px;
  opacity: 0;
}
</style>

<style lang="scss">
* {
  padding: 0;
  margin: 0;
}

#app {
  width: 90%;
  padding: 20px 5px;
  margin: 0 auto;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.pointer {
  cursor: pointer;

  * {
    cursor: pointer;
  }
}

</style>
