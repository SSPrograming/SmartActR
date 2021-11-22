<template>
  <div class="login">
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

    }
  }
}
</script>

<style scoped>
.form {
  width: 300px;
  padding: 20px;
  margin: calc(50vh - 200px) auto 0;
  box-shadow: hotpink 0 0 10px;
}
</style>