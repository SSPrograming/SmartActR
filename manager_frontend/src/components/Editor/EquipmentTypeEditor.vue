<template>
  <div class="equipment-type-editor">
    <el-form class="form" ref="form" :model="form" label-width="80px">
      <el-form-item label="图片" required>
        <el-upload
            class="image-uploader" ref="uploader"
            action="/api/v1/equipment/testPicUpload"
            :show-file-list="false"
            :auto-upload="false"
            :on-change="imageChange">
          <img v-if="imageUrl" :src="imageUrl" class="image" alt="">
          <i v-else class="el-icon-plus image-uploader-icon"></i>
        </el-upload>
      </el-form-item>
      <el-form-item style="text-align: center;">
        <el-button class="button" type="info" plain @click="$emit('editorCancel')">取消</el-button>
        <el-button class="button" type="primary" plain @click="submit">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "EquipmentTypeEditor",
  props: {
    form: Object,
  },
  data() {
    return {
      file: null
    }
  },
  computed: {
    imageUrl() {
      return this.file && URL.createObjectURL(this.file) || ''
    }
  },
  methods: {
    imageChange(file) {
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$utils.alertMessage(this, '上传图片大小不能超过 2MB！', 'error')
      } else {
        this.file = file.raw
      }
      return isLt2M
    },
    submit() {
      this.$refs.uploader.submit()
    }
  }
}
</script>

<style lang="scss">
.image-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.image-uploader .el-upload:hover {
  border-color: #409EFF;
}

.image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.image {
  width: 178px;
  display: block;
}
</style>