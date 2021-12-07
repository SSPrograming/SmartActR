<template>
  <div class="instruction-info-editor">
    <el-form class="form" ref="form" :model="form" label-width="80px">
      <el-form-item label="标题" required>
        <el-input v-model="form.instructionName" style="width: 250px" placeholder="请输入标题名称" clearable></el-input>
      </el-form-item>
      <el-form-item label="标签" required>
        <el-tag v-for="(tag, index) in form.instructionTags" :key="index" closable type="success"
                @close="removeTag(index)" disable-transitions>
          {{ tag }}
        </el-tag>
        <el-button icon="el-icon-plus" size="mini" circle @click="addTag" style="margin-left: 5px"></el-button>
      </el-form-item>
      <el-form-item label="图片" required>
        <el-upload class="image-uploader" ref="uploader" action="" :auto-upload="false"
                   :show-file-list="false" accept="image/*" :on-change="imageChange">
          <img :src="imageUrl" class="image" alt="" v-if="imageUrl">
          <i class="el-icon-plus image-uploader-icon" v-else></i>
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
  name: "InstructionInfoEditor",
  props: {
    form: {
      instructionID: Number,
      instructionName: String,
      instructionTags: Array,
      instructionCoverURL: String | File
    }
  },
  computed: {
    imageUrl() {
      if (typeof this.form.instructionCoverURL === 'object') {
        return this.form.instructionCoverURL && URL.createObjectURL(this.form.instructionCoverURL) || ''
      } else {
        return this.form.instructionCoverURL
      }
    }
  },
  methods: {
    addTag() {
      this.$prompt('请输入标签', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      }).then(({value}) => {
        if (!value.match(this.$utils.error.invalidToken)) {
          this.form.instructionTags.push(value)
        } else {
          this.$utils.alertMessage(this, '请勿输入特殊字符', 'warning')
        }
      }).catch(() => {
      });
    },
    removeTag(index) {
      this.form.instructionTags.splice(index, 1)
    },
    imageChange(file) {
      const isLt1M = file.size / 1024 / 1024 < 1
      const isImage = file.raw.type.match(/image/)
      if (!isImage) {
        this.$utils.alertMessage(this, '请上传图片文件', 'error')
      } else if (!isLt1M) {
        this.$utils.alertMessage(this, '上传图片大小不能超过1MB', 'error')
      } else {
        this.form.instructionCoverURL = file.raw
      }
      return isImage && isLt1M
    },
    submit() {
      this.$refs.form.validate().then((valid) => {
        if (!this.form.instructionName) {
          this.$utils.alertMessage(this, '请输入标题', 'warning')
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

  &:hover {
    border-color: #409EFF;
  }
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
  display: block;
  height: 178px;
}

</style>
