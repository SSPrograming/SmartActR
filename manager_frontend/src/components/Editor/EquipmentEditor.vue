<template>
  <div class="equipment-editor">
    <el-form class="form" ref="form" :model="form" label-width="80px">
      <el-form-item label="设备名称" required>
        <el-input v-model="form.equipmentName" style="width: 250px" placeholder="请输入设备名称" disabled></el-input>
      </el-form-item>
      <el-form-item label="设备编号" required>
        <el-input v-model="form.equipmentID" style="width: 250px" placeholder="请输入设备编号" disabled></el-input>
      </el-form-item>
      <el-form-item label="设备状态" required>
        <el-select v-model="form.equipmentStatus" placeholder="请选择">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
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
  name: "EquipmentEditor",
  props: {
    form: Object
  },
  data() {
    return {
      options: [
        {
          value: '完好',
          label: '完好'
        },
        {
          value: '损坏',
          label: '损坏'
        }
      ]
    }
  },
  methods: {
    submit() {
      this.$refs.form.validate().then((valid) => {
        if (valid) {
          this.$emit('editorConfirm')
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
