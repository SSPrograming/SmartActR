<template>
  <div id="app">
    <h1 v-if="!isLogin"><img class="logo" src="./assets/logo.png" alt="Logo"/>智慧活动室</h1>
    <div class="container">
      <aside v-if="!isLogin">
        <Sidebar></Sidebar>
      </aside>
      <main class="main">
        <router-view/>
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
      return this.$route.name === 'Login';
    }
  },
  mounted() {
    // 在卸载前删除本地存储的登陆状态
    window.addEventListener('beforeunload', () => {
      localStorage.removeItem('jwt');
    })
    this.$api.admin.getAdminName().then((res) => {
      console.log(res)
    })
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

h1 {
  display: flex;
  padding-left: calc(5% + 10px);
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
  width: 90%;
  margin: 0 auto;
}

aside {
  width: 240px;
}

main {
  flex: 1;
}

</style>
