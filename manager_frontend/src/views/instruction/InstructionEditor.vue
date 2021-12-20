<template>
  <div class="instruction-editor">
    <div class="container">
      <div class="header">
        <Toolbar back @back="$router.push({name: 'Instruction'})"></Toolbar>
        <el-button type="primary" plain @click="handleSave">保存</el-button>
      </div>
      <div class="editor">
        <MarkdownEditor :instruction="instruction"></MarkdownEditor>
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
      instructionID: 0,
      instruction: {
        content: '# SmartActR\n' +
            '\n' +
            '&emsp;&emsp;机械系科协活动室的管理系统——智慧活动室。\n' +
            '\n' +
            '## 分支\n' +
            '\n' +
            '+ `main`：每一次迭代发布的版本\n' +
            '+ `develop`：开发版本\n' +
            '+ `frontend`：前端分支\n' +
            '+ `backend`：后端分支\n' +
            '+ `manager-frontend`：管理端前端分支\n' +
            '+ `manager-backend`：管理端后端分支\n' +
            '+ `meeting`：会议记录\n' +
            '+ `doc`：文档\n' +
            '\n' +
            '```cpp\n' +
            '#include <iostream>\n' +
            'using namespace std;\n' +
            'int main() {\n' +
            '    cout << "Hello, world" << endl;\n' +
            '}\n' +
            '```',
        html: ''
      }
    }
  },
  mounted() {
    if (this.$route.query.instructionID) {
      this.instructionID = this.$route.query.instructionID
    } else {
      this.$router.push({name: 'Instruction'})
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
  padding-top: 5px;
}

.editor .v-note-wrapper {
  height: 50vh;
}
</style>
