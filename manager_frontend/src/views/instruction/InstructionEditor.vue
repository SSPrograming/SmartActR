<template>
  <div class="instruction-editor">
    <div class="container">
      <div class="header">
        <Toolbar back refresh @back="$router.push({name: 'Instruction'})"
                 @refresh="refresh"></Toolbar>
        <el-button type="primary" plain @click="handleSave">保存</el-button>
      </div>
      <div class="editor" v-loading="loading">
        <MarkdownEditor ref="MarkdownEditor" :instruction="instruction" @editorSave="handleSave"></MarkdownEditor>
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
      loading: false,
      instruction: {
        instructionID: 0,
        imageList: [],
        content: '',
        html: ''
      }
    }
  },
  mounted() {
    if (this.$route.query.instructionID) {
      this.instruction.instructionID = this.$route.query.instructionID
      this.getSingleInstruction()
      this.getSingleInstructionImageList()
    } else {
      this.$router.push({name: 'Instruction'})
    }
  },
  methods: {
    handleSave() {
      let formData = new FormData()
      formData.append('instructionID', this.instruction.instructionID)
      formData.append('instructionContent', this.instruction.content)
      this.$api.instruction.updateContent(formData).then((res) => {
        if (res.data.errCode === 0) {
          this.$utils.alertMessage(this, '保存成功', 'success')
        } else {
          this.$utils.error.APIError(this, res.data)
        }
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
      })
    },
    getSingleInstruction() {
      this.loading = true
      this.$api.instruction.getSingleInstruction({instructionID: this.instruction.instructionID}).then((res) => {
        if (res.data.errCode === 0) {
          this.instruction.content = res.data.instructionContent
          this.$utils.alertMessage(this, '获取数据成功', 'success')
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.loading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.loading = false
      })
    },
    getSingleInstructionImageList() {
      this.$api.instruction.getSingleInstructionImageList({instructionID: this.instruction.instructionID}).then((res) => {
        if (res.data.errCode === 0) {
          this.instruction.imageList = res.data.imageList
          this.$refs.MarkdownEditor.handleRefresh()
        } else {
          this.$utils.error.APIError(this, res.data)
        }
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
      })
    },
    refresh() {
      this.getSingleInstruction()
      // this.getSingleInstructionImageList()
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
  padding: 5px 0 10px 0;
}
</style>
