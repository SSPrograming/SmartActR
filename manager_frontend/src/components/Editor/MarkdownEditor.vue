<template>
  <div class="markdown-editor">
    <el-dialog :visible.sync="dialogVisible" top="5vh">
      <img class="dialog-image" :src="dialogImageUrl" alt="">
    </el-dialog>
    <div class="image-uploader">
      <el-upload action="" ref="imageUploader" list-type="picture-card" :auto-upload="false">
        <i slot="default" class="el-icon-plus"></i>
        <div class="image-file-container" slot="file" slot-scope="{file}">
          <img class="el-upload-list__item-thumbnail image-file" :src="file.url" alt="">
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
        <el-input class="input" :rows="24" type="textarea" placeholder="请输入内容" v-model="instruction.content"></el-input>
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
    instruction: Object
  },
  data() {
    return {
      dialogVisible: false,
      dialogImageUrl: '',
    }
  },
  mounted() {
    this.renderMarkdown()
  },
  methods: {
    renderMarkdown() {
      let hljs = require('highlight.js'); // https://highlightjs.org/
      let md = require('markdown-it')({
        html: true,
        xhtmlOut: false,
        breaks: false,
        langPrefix: 'language-',
        linkify: false,
        typographer: true,
        quotes: '“”‘’',
        highlight: function (str, lang) {
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
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    handleInsert(file) {
      console.log(file)
    },
    handleRemove(file) {
      this.$refs.imageUploader.handleRemove(file)
    }
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
    flex-basis: 50%;
    margin-right: 5px;
  }

  .right {
    flex-basis: 50%;
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
