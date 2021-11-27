<template>
  <div class="toolbar">
    <el-select class="choose-num"
               v-model="_showNums" placeholder="请选择" v-if="chooseNum">
      <el-option v-for="item in numOptions" :key="item.num"
                 :label="item.label" :value="item.num">
      </el-option>
    </el-select>
    <el-date-picker class="choose-date pointer" v-model="_queryStartDate" type="date" :editable="false"
                    placeholder="选择开始日期" v-if="chooseDate">
    </el-date-picker>
    <el-date-picker class="choose-date pointer" v-model="_queryEndDate" type="date" :editable="false"
                    placeholder="选择结束日期" v-if="chooseDate">
    </el-date-picker>
    <el-input class="input-query" placeholder="请输入查找内容" prefix-icon="el-icon-search"
              v-model="_queryStr" v-if="query">
    </el-input>
    <el-button type="info" @click="$emit('query')" v-if="query">查找</el-button>
  </div>
</template>

<script>
export default {
  name: "ToolBar",
  props: {
    chooseNum: Boolean,
    chooseDate: Boolean,
    query: Boolean,
    showNums: Number,
    queryStartDate: Date,
    queryEndDate: Date,
    queryStr: String
  },
  data() {
    return {
      numOptions: [
        {
          label: '查看近20条',
          num: 20
        },
        {
          label: '查看近50条',
          num: 50
        },
        {
          label: '查看近100条',
          num: 100
        },
        {
          label: '查看近500条',
          num: 500
        },
        {
          label: '查看全部',
          num: -1
        }
      ]
    }
  },
  computed: {
    _showNums: {
      get() {
        return this.showNums
      },
      set(val) {
        this.$emit('showNumsChange', val)
      }
    },
    _queryStartDate: {
      get() {
        return this.queryStartDate
      },
      set(val) {
        this.$emit('queryStartDateChange', val)
      }
    },
    _queryEndDate: {
      get() {
        return this.queryEndDate
      },
      set(val) {
        this.$emit('queryEndDateChange', val)
      }
    },
    _queryStr: {
      get() {
        return this.queryStr
      },
      set(val) {
        this.$emit('queryStrChange', val)
      }
    }
  }
}
</script>

<style scoped lang="scss">
.toolbar {
  display: flex;

  * {
    margin: 0 5px;
  }
}

.choose-num {
  flex-basis: 300px;
}

.choose-date {
  flex-basis: 400px;
}

.input-query {
  flex-basis: 400px;
}

</style>