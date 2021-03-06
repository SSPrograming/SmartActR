<template>
  <div class="rule-editor">
    <div class="container">
      <el-form class="form" ref="form" :model="form" label-width="80px">
        <el-form-item label="重复" required>
          <el-select v-model="form.repeat" placeholder="请选择" :disabled="edit">
            <el-option v-for="item in repeatOptions" :key="item.value" :label="item.label"
                       :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="星期" required v-if="form.repeat">
          <el-select v-model="form.day" placeholder="请选择">
            <el-option v-for="item in dayOptions" :key="item.value" :label="item.label"
                       :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="日期" required v-if="!form.repeat">
          <el-date-picker class="pointer" v-model="form.date" type="date" :editable="false"
                          placeholder="请选择日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="开始时间" required>
          <el-time-select class="pointer" v-model="form.startTime" :picker-options="timeOptions" :editable="false"
                          placeholder="请选择开始时间"></el-time-select>
        </el-form-item>
        <el-form-item label="结束时间" required>
          <el-time-select class="pointer" v-model="form.endTime" :picker-options="timeOptions" :editable="false"
                          placeholder="请选择结束时间"></el-time-select>
        </el-form-item>
        <el-form-item label="失效日期" required v-if="form.repeat">
          <el-date-picker class="pointer" v-model="form.expireDate" type="date" :editable="false"
                          placeholder="请选择失效日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="规则描述">
          <el-input type="textarea" :rows="5" placeholder="请输入规则描述" v-model="form.ruleDescription"></el-input>
        </el-form-item>
        <div style="text-align: center;">
          <el-button class="button" type="info" plain @click="$emit('editorCancel')">取消</el-button>
          <el-button class="button" type="danger" plain @click="handleDelete" v-if="edit">删除</el-button>
          <el-button class="button" type="primary" plain @click="submit">提交</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "RuleEditor",
  props: {
    form: {
      ruleID: Number,
      repeat: Boolean,
      day: Number,
      date: Date,
      startTime: String,
      endTime: String,
      expireDate: Date,
      ruleDescription: String
    }
  },
  data() {
    return {
      repeatOptions: [
        {
          value: false,
          label: '否'
        },
        {
          value: true,
          label: '是'
        }
      ],
      dayOptions: [
        {
          value: 1,
          label: '一'
        },
        {
          value: 2,
          label: '二'
        },
        {
          value: 3,
          label: '三'
        },
        {
          value: 4,
          label: '四'
        },
        {
          value: 5,
          label: '五'
        },
        {
          value: 6,
          label: '六'
        },
        {
          value: 0,
          label: '日'
        },
      ],
      timeOptions: {
        start: '08:00',
        step: '00:30',
        end: '22:00'
      }
    }
  },
  computed: {
    edit() {
      return Boolean(this.form.ruleID)
    }
  },
  methods: {
    handleDelete() {
      this.$confirm('此操作将删除该规则, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$emit('editorDelete')
      }).catch(() => {
      })
    },
    submit() {
      this.$refs.form.validate().then((valid) => {
        if (!this.form.repeat && !this.form.date) {
          this.$utils.alertMessage(this, '请选择日期', 'warning')
        } else if (this.form.repeat && typeof this.form.day != "number") {
          this.$utils.alertMessage(this, '请选择星期', 'warning')
        } else if (!this.form.startTime) {
          this.$utils.alertMessage(this, '请选择开始时间', 'warning')
        } else if (!this.form.endTime) {
          this.$utils.alertMessage(this, '请选择结束时间', 'warning')
        } else if (this.form.endTime <= this.form.startTime) {
          this.$utils.alertMessage(this, '请选择正确的时间范围', 'warning')
        } else if (this.form.repeat && !this.form.expireDate) {
          this.$utils.alertMessage(this, '请选择失效日期', 'warning')
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

<style scoped lang="scss">

</style>
