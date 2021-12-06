<template>
  <div class="equipment-rules">
    <el-dialog title="规则编辑" :visible.sync="showRuleEditor" v-loading="dialogLoading">
      <RuleEditor :form="form" @editorCancel="editorCancel" @editorDelete="handleDelete"
                  @editorConfirm="editorConfirm"></RuleEditor>
    </el-dialog>
    <div class="container">
      <div class="header">
        <Toolbar refresh @refresh="getRules"></Toolbar>
        <el-button type="primary" plain @click="handleAdd">添加规则</el-button>
      </div>
      <el-calendar class="calendar" v-loading="calendarLoading">
        <template slot="dateCell" slot-scope="{date/*, data*/}">
          <div class="calendar-date"> {{ date.getDate() }}</div>
          <div class="calendar-rule" v-for="item in getDayRules(date)" :key="item.ruleID">
            <div :class="item.repeat ? 'repeat' : 'once'" @click="handleEdit(item)">
              {{ item.startTime }} ~ {{ item.endTime }}
            </div>
          </div>
        </template>
      </el-calendar>
    </div>
  </div>
</template>

<script>
import Toolbar from '@/components/Toolbar'
import RuleEditor from '@/components/Editor/RuleEditor'

export default {
  name: "EquipmentRules",
  components: {
    RuleEditor,
    Toolbar
  },
  data() {
    return {
      dialogLoading: false,
      calendarLoading: false,
      rules: [],
      showRuleEditor: false,
      editRuleID: null,
      form: {
        ruleID: null,
        repeat: false,
        day: null,
        date: null,
        startTime: null,
        endTime: null,
        expireDate: null,
        ruleDescription: ''
      }
    }
  },
  mounted() {
    this.getRules()
  },
  methods: {
    getRules() {
      this.calendarLoading = true
      this.$api.rule.getRules().then((res) => {
        if (res.data.errCode === 0) {
          this.rules = res.data.rules
          this.$utils.alertMessage(this, '获取数据成功', 'success')
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.calendarLoading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.calendarLoading = false
      })
    },
    getDayRules(date) {
      let result = []
      this.rules.forEach((rule) => {
        // 有效的规则
        if (date <= new Date(rule.expireDate) && date >= new Date(rule.takeEffectDate)) {
          // 重复规则
          if (rule.repeat) {
            if (rule.day === date.getDay()) {
              result.push(rule)
            }
          }
          // 非重复规则
          else {
            let ruleDate = new Date(rule.date)
            ruleDate.setHours(0)
            if (date.getFullYear() === ruleDate.getFullYear()
                && date.getMonth() === ruleDate.getMonth()
                && date.getDate() === ruleDate.getDate()) {
              result.push(rule)
            }
          }
        }
      })
      const sortType = {
        prop: 'startTime',
        order: 'ascending'
      }
      this.$utils.sort(result, sortType)
      return result
    },
    handleAdd() {
      if (this.editRuleID) {
        this.editRuleID = null
        this.form = {
          ruleID: null,
          repeat: false,
          day: null,
          date: null,
          startTime: null,
          endTime: null,
          expireDate: null,
          ruleDescription: ''
        }
      }
      this.showRuleEditor = true
    },
    handleEdit(rule) {
      this.editRuleID = rule.ruleID
      this.form = {
        ...rule,
        date: new Date(rule.date),
        expireDate: new Date(rule.expireDate)
      }
      this.showRuleEditor = true
    },
    handleDelete() {
      if (this.editRuleID) {
        this.dialogLoading = true
        this.$api.rule.deleteRule({ruleID: this.editRuleID}).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '删除成功', 'success')
            this.getRules()
          } else {
            this.$utils.error.APIError(this, res.data)
          }
          this.dialogLoading = false
          this.showRuleEditor = false
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.dialogLoading = false
          this.showRuleEditor = false
        })
      } else {
        this.showRuleEditor = false
      }
    },
    editorCancel() {
      this.showRuleEditor = false
    },
    editorConfirm() {
      let params = {
        ...this.form,
        day: this.form.repeat && this.form.day,
        date: !this.form.repeat && this.$utils.time.format(this.form.date, 'yyyy-MM-dd'),
        expireDate: this.form.repeat && this.$utils.time.format(this.form.expireDate, 'yyyy-MM-dd')
      }
      this.dialogLoading = true
      // 新建
      if (!this.editRuleID) {
        this.$api.rule.addRule(params).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '添加成功', 'success')
            this.form = {
              ruleID: null,
              repeat: false,
              day: null,
              date: null,
              startTime: null,
              endTime: null,
              expireDate: null,
              ruleDescription: ''
            }
            this.getRules()
          } else {
            this.$utils.error.APIError(this, res.data)
          }
          this.dialogLoading = false
          this.showRuleEditor = false
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.dialogLoading = false
          this.showRuleEditor = false
        })
      }
      // 编辑
      else {
        params = {
          ...params,
          ruleID: this.editRuleID
        }
        this.$api.rule.updateRule(params).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '编辑成功', 'success')
            this.getRules()
          } else {
            this.$utils.error.APIError(this, res.data)
          }
          this.dialogLoading = false
          this.showRuleEditor = false
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.dialogLoading = false
          this.showRuleEditor = false
        })
      }
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

.calendar {
  .calendar-rule {
    margin-top: 5px;
    font-size: 14px;

    .repeat {
      padding: 1px 5px;
      background: $--color-repeat;

      &:focus, &:hover {
        background: mix($--color-repeat, $--color-white, 75%);
      }

      &:active {
        background: mix($--color-repeat, $--color-black, 75%);
      }
    }

    .once {
      padding: 1px 5px;
      background: $--color-once;

      &:focus, &:hover {
        background: mix($--color-once, $--color-white, 75%);
      }

      &:active {
        background: mix($--color-once, $--color-black, 75%);
      }
    }
  }
}
</style>

<style lang="scss">
.el-calendar-table .el-calendar-day {
  height: auto;
  min-height: 85px;
}
</style>
