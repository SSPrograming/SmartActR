<template>
  <div class="feedback-editor">
    <el-form class="form" ref="form" :model="form" label-width="80px">
      <el-form-item label="提交人">
        <!--
        <el-input style="width: 250px" v-model="form.userName" disabled></el-input>
        -->
        <div style="width: 200px;
                    padding: 0 15px;
                    border: 1px solid rgb(220, 223, 230);
                    border-radius: 4px;">
          {{ form.userName }}
        </div>
      </el-form-item>
      <el-form-item label="提交时间">
        <!--
        <el-date-picker class="pointer" v-model="form.postDate" type="date" disabled></el-date-picker>
        -->
        <div style="width: 200px;
                    padding: 0 15px;
                    border: 1px solid rgb(220, 223, 230);
                    border-radius: 4px;">
          {{ form.postDate }}
        </div>
      </el-form-item>
      <el-form-item label="反馈内容">
        <!--
        <el-input type="textarea" :rows="10" v-model="form.feedbackContent"></el-input>
        -->
        <div style="width: 90%;
                    min-height: 200px;
                    padding: 0 15px;
                    border: 1px solid rgb(220, 223, 230);
                    border-radius: 4px;">
          {{ form.feedbackContent }}
        </div>
      </el-form-item>
      <div style="text-align: center;">
        <el-button class="button" type="info" plain @click="$emit('editorCancel')">取消</el-button>
        <el-button class="button" type="primary" plain @click="$emit('editorConfirm')">确定</el-button>
      </div>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "FeedbackEditor",
  props: {
    form: Object
  }
}
</script>

<style scoped lang="scss">
.feedback-content {
  width: 100%;
  min-height: 200px;
  border: 1px solid rgb(220, 223, 230);
  border-radius: 4px;
}
</style>