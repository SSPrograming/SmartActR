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
      rules: [
        {
          ruleID: 1,
          repeat: 0,
          day: 0,
          date: "2021-12-4",
          startTime: "08:00",
          endTime: "12:00",
          expireDate: "2021-12-31",
          description: ''
        },
        {
          ruleID: 2,
          repeat: 1,
          day: 0,
          date: "2021-12-4",
          startTime: "13:00",
          endTime: "18:00",
          expireDate: "2021-12-31",
          description: ''
        },
        {
          ruleID: 3,
          repeat: 0,
          day: 0,
          date: "2021-12-26",
          startTime: "08:00",
          endTime: "12:00",
          expireDate: "2021-12-31",
          description: ''
        }
      ],
      showRuleEditor: false,
      editRuleID: null,
      form: {
        ruleID: 0,
        repeat: 0,
        day: null,
        date: null,
        startTime: null,
        endTime: null,
        expireDate: null,
        description: ''
      }
    }
  },
  methods: {
    getRules() {

    },
    getDayRules(date) {
      let result = []
      this.rules.forEach((rule) => {
        // 有效的规则
        if (date <= new Date(rule.expireDate)) {
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
          ruleID: 0,
          repeat: 0,
          day: null,
          date: null,
          startTime: null,
          endTime: null,
          expireDate: null,
          description: ''
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
      this.showRuleEditor = false
    },
    editorCancel() {
      this.showRuleEditor = false
    },
    editorConfirm() {
      console.log(this.form)
      this.showRuleEditor = false
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
      background: lightsteelblue;

      &:focus, &:hover {
        background: mix(lightsteelblue, $--color-white, 75%);
      }

      &:active {
        background: mix(lightsteelblue, $--color-black, 75%);
      }
    }

    .once {
      padding: 1px 5px;
      background: lightgreen;

      &:focus, &:hover {
        background: mix(lightgreen, $--color-white, 75%);
      }

      &:active {
        background: mix(lightgreen, $--color-black, 75%);
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
