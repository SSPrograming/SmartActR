<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link>
      |
      <router-link to="/about">About</router-link>
    </div>
    <el-menu :default-active="0" class="el-menu-demo" mode="horizontal">
      <router-link to="/">
        <el-menu-item index="1">
          Home
        </el-menu-item>
      </router-link>
      <router-link to="/about">
        <el-menu-item index="2">
          About
        </el-menu-item>
      </router-link>
    </el-menu>
    <router-view/>
  </div>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
