<template>
  <div class="notice-editor">
    <el-form class="form" ref="form" :model="form" label-width="80px">
      <el-form-item label="过期时间" required>
        <el-date-picker class="pointer" v-model="form.expireDate" type="date" :editable="false" placeholder="选择过期时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="公告内容">
        <el-input type="textarea" :rows="10" placeholder="请输入公告内容" v-model="form.noticeContent">
        </el-input>
      </el-form-item>
      <div style="text-align: center;">
        <el-button class="button" type="info" plain @click="$emit('editorCancel')">取消</el-button>
        <el-button class="button" type="primary" plain @click="submit">提交</el-button>
      </div>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "NoticeEditor",
  props: {
    form: Object
  },
  methods: {
    submit() {
      this.$refs.form.validate().then((valid) => {
        if (!this.form.expireDate) {
          this.$utils.alertMessage(this, '请设置过期时间', 'warning')
        } else {
          if (valid) {
            this.$emit('editorConfirm')
          }
        }
      })
    }
  }
}
</script>

<style scoped lang="scss">

</style>