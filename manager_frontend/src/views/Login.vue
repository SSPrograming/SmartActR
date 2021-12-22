<template>
  <div class="login" v-loading.fullscreen="loading">
    <div class="container">
      <div class="title">
        管理员登录
      </div>
      <el-form class="form" ref="form" :model="form" label-width="80px">
        <el-form-item label="用户名" @keyup.enter.native="onSubmit">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" @keyup.enter.native="onSubmit">
          <el-input v-model="form.password" show-password></el-input>
        </el-form-item>
        <div style="text-align: center; padding: 10px;">
          <el-button type="primary" @click="onSubmit">登录</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      loading: false,
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      const params = {
        username: this.form.username,
        password: this.$utils.password.getHash(this.form.username, this.form.password)
      }
      this.$api.admin.login(params).then((res) => {
        if (res.data.errCode === 0) {
          this.$store.commit({
            type: 'login',
            jwt: res.data.jwt
          })
          this.$utils.alertMessage(this, '登录成功', 'success')
          this.$router.push({
            name: 'Home'
          })
        } else {
          console.log(this.$utils.password.getHash(this.form.username, this.form.password))
          this.$utils.error.APIError(this, res.data)
        }
        this.loading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.loading = false
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
