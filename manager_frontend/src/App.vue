<template>
  <div id="app">
    <el-scrollbar class="scrollbar">
      <header>
        <h1><img class="logo" src="./assets/logo.png" alt="Logo"/>智慧活动室</h1>
        <el-button v-if="!isLogin" type="primary" plain @click="logout">登出</el-button>
      </header>
      <el-divider class="divider"></el-divider>
      <div class="container">
        <transition name="sidebar">
          <aside v-if="!isLogin">
            <Sidebar></Sidebar>
          </aside>
        </transition>
        <main class="main" :style="isLogin?'width: 100%;padding:0'
        :'width: calc(95% - 240px);padding: 0 calc(5% + 20px) 0 20px;'">
          <router-view></router-view>
        </main>
      </div>
    </el-scrollbar>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar";

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

h1 {
  padding: 0;
  margin: 0;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 5%;

  h1 {
    display: flex;
    padding-left: 10px;
    font-family: '微软雅黑', sans-serif;
    color: $--color-primary;
    line-height: 50px;
    cursor: default;

    .logo {
      width: 50px;
      margin-right: 15px;
    }
  }
}

.divider {
  width: 90%;
  margin-left: auto;
  margin-right: auto;
}

.container {
  display: flex;
  margin: 0 auto;

  aside {
    width: 240px;
    padding-left: 5%;
  }

  main {
    box-sizing: border-box;
  }
}

.sidebar-enter-active, .sidebar-leave-active {
  transition: all .5s ease-in-out;
}

.sidebar-enter, .sidebar-leave-to {
  margin-left: calc(-240px - 5%);
  opacity: 0;
}
</style>

<style lang="scss">
html, body {
  padding: 0;
  margin: 0;
}

#app {
  height: 100vh;
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

.scrollbar {
  height: 100%;

  & > .el-scrollbar__wrap {
    overflow-x: hidden;
  }
}

</style>
