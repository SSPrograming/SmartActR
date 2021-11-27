<template>
  <div class="login">
    <div class="title">
      智慧活动室
    </div>
    <el-form class="form" ref="form" :model="form" label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="form.username"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" show-password></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit() {
      this.$store.commit({
        type: 'login',
        jwt: 'jwt'
      })
      this.$router.push({
        name: 'Home'
      })
    }
  }
}
</script>

<style scoped>

.title {
  margin: calc(50vh - 300px) auto 50px;
  color: hotpink;
  font-size: 48px;
}

.form {
  width: 300px;
  padding: 40px 20px 20px;
  margin: 0 auto;
  box-shadow: hotpink 0 0 10px;
  border-radius: 20px;
}
</style>