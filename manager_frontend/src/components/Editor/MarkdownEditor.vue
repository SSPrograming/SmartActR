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
  </div>
</template>

<script>
export default {
  name: "MarkdownEditor",
  data() {
    return {
      dialogVisible: false,
      dialogImageUrl: '',
    }
  },
  methods: {
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
  }
}
</script>

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
    line-height: 107px;
  }

  .el-upload-list--picture-card .el-upload-list__item-actions span + span {
    margin-left: 10px;
  }
}
</style>

<style scoped lang="scss">
.dialog-image {
  display: block;
  max-width: 100%;
  max-height: 75vh;
  margin: 0 auto;
}
</style>