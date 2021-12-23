<template>
  <div class="markdown-editor">
    <el-dialog :visible.sync="dialogVisible" top="10vh">
      <img class="dialog-image" :src="dialogImageUrl" alt="">
    </el-dialog>
    <div class="image-uploader">
      <el-upload ref="imageUploader" action="" :auto-upload="true" list-type="picture-card" accept="image/*"
                 :before-upload="handleBefore" :http-request="handleUpload" :on-success="handleSuccess"
                 :on-error="handleError">
        <i slot="default" class="el-icon-plus"></i>
        <div class="image-file-container" slot="file" slot-scope="{file}">
          <img class="el-upload-list__item-thumbnail image-file" :src="file.url" alt="">
          <el-progress
              v-if="file.status === 'uploading'" type="circle" :stroke-width="6" :width="80"
              :percentage="parsePercentage(file.percentage)">
          </el-progress>
          <span class="el-upload-list__item-actions">
            <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
              <i class="el-icon-zoom-in"></i>
            </span>
            <span class="el-upload-list__item-preview" @click="handleInsert(file)">
              <i class="el-icon-paperclip"></i>
            </span>
            <span class="el-upload-list__item-delete" @click="handleRemove(file)">
              <i class="el-icon-delete"></i>
            </span>
          </span>
        </div>
      </el-upload>
    </div>
    <div class="main">
      <div class="left">
        <el-input ref="input" class="input" type="textarea" v-model="instruction.content" placeholder="请输入内容"
                  :rows="24" @keydown.native="handleHotkey"></el-input>
      </div>
      <div class="right">
        <el-scrollbar class="scrollbar" style="height: 100%">
          <div class="output" v-html="instruction.html"></div>
        </el-scrollbar>
      </div>
    </div>
  </div>
</template>

<script>
import 'highlight.js/styles/github-gist.css'

export default {
  name: "MarkdownEditor",
  props: {
    instruction: {
      instructionID: Number,
      imageList: Array,
      content: String,
      html: String
    }
  },
  data() {
    return {
      dialogVisible: false,
      dialogImageUrl: ''
    }
  },
  mounted() {
    this.renderMarkdown()
  },
  methods: {
    renderMarkdown() {
      const hljs = require('highlight.js') // https://highlightjs.org/
      const md = require('markdown-it')({
        html: true,
        xhtmlOut: false,
        breaks: false,
        langPrefix: 'language-',
        linkify: false,
        typographer: true,
        quotes: '“”‘’',
        highlight(str, lang) {
          if (lang && hljs.getLanguage(lang)) {
            try {
              return '<pre class="hljs">' +
                  hljs.highlight(str, {language: lang, ignoreIllegals: true}).value +
                  '</pre>';
              // eslint-disable-next-line no-empty
            } catch (__) {
            }
          }
          return '<pre class="hljs">' + md.utils.escapeHtml(str) + '</pre>';
        }
      });
      this.instruction.html = md.render(this.instruction.content);
    },
    checkFileStatus(file) {
      if (file.status !== 'success') {
        this.$utils.alertMessage(this, '正在上传中', 'warning')
        return false
      }
      return true
    },
    handlePictureCardPreview(file) {
      if (!this.checkFileStatus(file)) {
        return
      }
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    },
    handleInsert(file) {
      if (!this.checkFileStatus(file)) {
        return
      }
      const textarea = this.$refs.input.$refs.textarea
      const input = `![](${file.url.replaceAll(' ', '%20')})`
      let startPos = 0
      if (textarea.selectionStart || textarea.selectionStart === 0) {
        startPos = textarea.selectionStart
        this.instruction.content = this.instruction.content.substring(0, startPos)
            + input + this.instruction.content.substring(textarea.selectionEnd)
      } else {
        startPos = this.instruction.content.length
        this.instruction.content += input
      }
      textarea.focus()
      this.$nextTick(() => {
        textarea.setSelectionRange(startPos, startPos + input.length)
      })
    },
    handleRemove(file) {
      if (!this.checkFileStatus(file)) {
        return
      }
      const params = {
        instructionID: this.instruction.instructionID,
        instructionImageID: file.instructionImageID
      }
      this.$api.instruction.deleteImage(params).then((res) => {
        if (res.data.errCode === 0) {
          this.$utils.alertMessage(this, '删除成功', 'success')
          this.$refs.imageUploader.handleRemove(file)
        } else {
          this.$utils.error.APIError(this, res.data)
        }
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
      })
    },
    handleHotkey(event) {
      // Ctrl + S
      if (event.ctrlKey && event.keyCode === 83) {
        event.preventDefault()
        this.$emit('editorSave')
      }
      // Tab
      else if (event.keyCode === 9) {
        event.preventDefault()
        const textarea = this.$refs.input.$refs.textarea
        const input = '    '
        let startPos = 0
        if (textarea.selectionStart || textarea.selectionStart === 0) {
          startPos = textarea.selectionStart
          this.instruction.content = this.instruction.content.substring(0, startPos)
              + input + this.instruction.content.substring(textarea.selectionEnd)
        } else {
          startPos = this.instruction.content.length
          this.instruction.content += input
        }
        this.$nextTick(() => {
          textarea.setSelectionRange(startPos + input.length, startPos + input.length)
        })
      }
    },
    handleBefore(file) {
      const isLt1M = file.size / 1024 / 1024 < 10
      const isImage = file.type.match(/image/)
      if (!isImage) {
        this.$utils.alertMessage(this, '请上传图片文件', 'error')
      } else if (!isLt1M) {
        this.$utils.alertMessage(this, '上传图片大小不能超过10MB', 'error')
      }
      return isImage && isLt1M
    },
    handleUpload(params) {
      let formData = new FormData()
      formData.append('instructionID', this.instruction.instructionID)
      formData.append('file', params.file)
      return this.$api.instruction.addImage(formData, this.$refs.imageUploader.handleProgress, params.file)
    },
    handleSuccess(res, file, fileList) {
      if (res.data.errCode === 0) {
        file.instructionImageID = res.data.instructionImageID
        file.url = res.data.ImageURL
        this.$utils.alertMessage(this, '上传成功', 'success')
      } else {
        this.$utils.error.APIError(this, res.data)
        fileList.splice(fileList.indexOf(file), 1)
      }
    },
    handleError(err, /*file, fileList*/) {
      this.$utils.error.ServerError(this, err)
      // fileList.splice(fileList.indexOf(file), 1)
    },
    handleRefresh() {
      this.$refs.imageUploader.fileList.splice(0, this.$refs.imageUploader.fileList.length)
      this.instruction.imageList.forEach((image) => {
        this.$refs.imageUploader.fileList.push({
          instructionImageID: image.instructionImageID,
          url: image.imageURL
        })
      })
    },
    parsePercentage(val) {
      return parseInt(val, 10);
    },
  },
  watch: {
    'instruction.content'() {
      this.renderMarkdown()
    }
  }
}
</script>

<style scoped lang="scss">
.dialog-image {
  display: block;
  max-width: 100%;
  max-height: 75vh;
  margin: 0 auto;
}

.main {
  display: flex;
  width: 100%;

  .left {
    width: 50%;
    margin-right: 5px;
  }

  .right {
    width: 50%;
    height: 32em;
    margin-left: 5px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;

    .output {
      box-sizing: border-box;
      padding: 20px;
      font-size: 14px;
    }
  }
}

</style>

<style lang="scss">
.image-uploader {
  .image-file-container {
    text-align: center;
    height: 100%;

    .image-file {
      width: auto;
      max-width: 100%;
      height: auto;
      max-height: 100%;
      margin: auto;
    }
  }

  .el-upload-list__item {
    width: auto;
    min-width: 100px;
    height: 100px;
  }

  .el-upload--picture-card {
    width: 100px;
    height: 100px;
    margin: 0 8px 12px 0;
    line-height: 107px;
  }

  .el-upload-list--picture-card .el-upload-list__item-actions span + span {
    margin-left: 10px;
  }

  .el-upload-list--picture-card .el-progress {
    width: 80px;
  }
}

.output {
  color: #24292f;

  h1 {
    padding-bottom: .3em;
    border-bottom: 1px solid #d8dee4;
  }

  h2 {
    padding-bottom: .3em;
    border-bottom: 1px solid #d8dee4;
  }

  hr {
    height: .1em;
    padding: 0;
    margin: 24px 0;
    background-color: #d0d7de;
    border: 0;
  }

  img {
    max-width: 100%;
    background: #ffffff;
  }

  blockquote {
    margin: 0;
    padding: 0 1em;
    font-size: 14px;
    color: #57606a;
    border-left: .25em solid #d0d7de;
  }

  pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: #f6f8fa;
    border-radius: 6px;
    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
  }

  code {
    padding: .2em .4em;
    margin: 0;
    font-size: 85%;
    background-color: #afb8c133;
    border-radius: 6px;
  }

  ul {
    margin: 0;
    padding-left: 2em;
  }
}

.input {
  textarea::-webkit-scrollbar {
    width: 6px;
    height: 8px;
    background-color: #ebeef5;
  }

  textarea:hover::-webkit-scrollbar-thumb {
    background-color: rgba(144, 147, 153, 0.3);
  }

  textarea::-webkit-scrollbar-thumb {
    background-color: rgba(144, 147, 153, 0);
    border-radius: 3px;
  }

  textarea::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 1);
  }
}

</style>
