<template>
  <div class="login">
    <div class="container">
      <div class="title">
        管理员登录
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
      console.log(this.$utils.password.getHash(this.form.username, this.form.password))
      this.$store.commit({
        type: 'login',
        jwt: 'jwt'
      })
      this.$utils.alertMessage(this, '登录成功', 'success');
      this.$router.push({
        name: 'Home'
      })
    }
  }
}
</script>

<style scoped lang="scss">
@import "src/element-variables";

.login {
  text-align: center;
}

.title {
  padding: 10vh 0 30px;
  margin: auto;
  color: $--color-primary;
  font-size: $--my-font-size-huge;
}

.form {
  width: 300px;
  padding: 40px 20px 20px;
  margin: 0 auto;
  box-shadow: $--color-primary 0 0 10px;
  border-radius: 20px;
}
</style>
