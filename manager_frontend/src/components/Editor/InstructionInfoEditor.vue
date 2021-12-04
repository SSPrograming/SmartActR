<template>
  <div class="instruction-info-editor">
    <el-form class="form" ref="form" :model="form" label-width="80px">
      <el-form-item label="标题" required>
        <el-input v-model="form.instructionName" style="width: 250px" placeholder="请输入设备名称"></el-input>
      </el-form-item>
      <el-form-item label="标签" required>
        <el-tag v-for="(tag, index) in form.instructionTags" :key="index" closable type="info"
                @close="removeTag(index)" disable-transitions>
          {{ tag }}
        </el-tag>
        <el-button icon="el-icon-plus" circle size="mini" @click="addTag" style="margin-left: 5px"></el-button>
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
  name: "InstructionInfoEditor",
  props: {
    form: Object
  },
  methods: {
    addTag() {
      this.$prompt('请输入标签', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({value}) => {
        this.form.instructionTags.push(value)
      }).catch(() => {
      });
    },
    removeTag(index) {
      this.form.instructionTags.splice(index, 1)
    },
    submit() {

    }
  }
}
</script>

<style scoped>

</style>