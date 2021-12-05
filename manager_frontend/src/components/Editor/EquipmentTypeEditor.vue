<template>
  <div class="equipment-type-editor">
    <el-form class="form" ref="form" :model="form" label-width="80px">
      <el-form-item label="设备名称" required>
        <el-input v-model="form.equipmentName" style="width: 250px" placeholder="请输入设备名称" clearable></el-input>
      </el-form-item>
      <el-form-item label="设备数量" required>
        <el-input-number v-model="form.equipmentCount" :min="1" :disabled="!add"></el-input-number>
      </el-form-item>
      <el-form-item label="设备描述" required>
        <el-input type="textarea" :rows="5" maxlength="50" show-word-limit placeholder="请输入设备描述"
                  v-model="form.equipmentDescription">
        </el-input>
      </el-form-item>
      <el-form-item label="图片" required>
        <el-upload
            class="image-uploader" ref="uploader"
            action=""
            accept="image/*"
            :show-file-list="false"
            :auto-upload="false"
            :on-change="imageChange">
          <img v-if="imageUrl" :src="imageUrl" class="image" alt="">
          <i v-else class="el-icon-plus image-uploader-icon"></i>
        </el-upload>
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
  name: "EquipmentTypeEditor",
  props: {
    form: Object,
    add: Boolean
  },
  computed: {
    imageUrl() {
      if (typeof this.form.equipmentImage === 'object') {
        return this.form.equipmentImage && URL.createObjectURL(this.form.equipmentImage) || ''
      } else {
        return this.form.equipmentImage
      }
    }
  },
  methods: {
    imageChange(file) {
      const isLt1M = file.size / 1024 / 1024 < 1
      const isImage = file.raw.type.match(/image/)
      if (!isImage) {
        this.$utils.alertMessage(this, '请上传图片文件', 'error')
      } else if (!isLt1M) {
        this.$utils.alertMessage(this, '上传图片大小不能超过1MB', 'error')
      } else {
        this.form.equipmentImage = file.raw
      }
      return isImage && isLt1M
    },
    submit() {
      this.$refs.form.validate().then((valid) => {
        if (!this.form.equipmentName) {
          this.$utils.alertMessage(this, '请输入设备名称', 'warning')
        } else if (!this.form.equipmentCount) {
          this.$utils.alertMessage(this, '请输入设备数量', 'warning')
        } else if (!this.form.equipmentDescription) {
          this.$utils.alertMessage(this, '请输入设备描述', 'warning')
        } else if (!this.form.equipmentImage) {
          this.$utils.alertMessage(this, '请上传图片', 'warning')
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
  height: 178px;
  display: block;
}

</style>
