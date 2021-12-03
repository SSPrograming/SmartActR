<template>
  <div class="instruction-editor">
    <div class="container">
      <div class="header">
        <Toolbar back @back="$router.push({name: 'Instruction'})"></Toolbar>
        <el-button type="primary" plain @click="handleSave">保存</el-button>
      </div>
      <div class="editor">
        <MarkdownEditor></MarkdownEditor>
      </div>
    </div>
  </div>
</template>

<script>
import Toolbar from '@/components/Toolbar'
import MarkdownEditor from '@/components/Editor/MarkdownEditor'

export default {
  name: "InstructionEditor",
  components: {
    Toolbar,
    MarkdownEditor
  },
  data() {
    return {
      instruction: {
        content: '',
        html: ''
      }
    }
  },
  methods: {
    handleSave() {
      console.log(this.html)
    },
    setHTML(content, html) {
      this.html = html
    }
  }
}
</script>

<style scoped lang="scss">
@import "src/element-variables";

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: $--toolbar-margin-bottom;
}

.editor {
  padding-top: 20px;
}

.editor .v-note-wrapper {
  height: 50vh;
}
</style>
