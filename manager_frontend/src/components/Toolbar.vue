<template>
  <div class="toolbar">
    <el-button type="primary" icon="el-icon-back" plain @click="$emit('back')" v-if="back"></el-button>
    <el-select class="choose-num" v-model="toolbar.showNums" placeholder="请选择" @change="$emit('query')"
               v-if="chooseNum">
      <el-option v-for="item in numOptions" :key="item.value" :label="item.label" :value="item.value">
      </el-option>
    </el-select>
    <el-date-picker class="choose-date pointer" v-model="toolbar.queryStartDate" type="date" placeholder="选择开始日期"
                    :editable="false" @change="toolbar.queryEndDate && $emit('query')" v-if="chooseDate">
    </el-date-picker>
    <el-date-picker class="choose-date pointer" v-model="toolbar.queryEndDate" type="date" placeholder="选择结束日期"
                    :editable="false" @change="toolbar.queryStartDate && $emit('query')" v-if="chooseDate">
    </el-date-picker>
    <el-input class="input-query" v-model="toolbar.queryStr" placeholder="请输入查找内容"
              prefix-icon="el-icon-search" @keyup.enter.native="$emit('query')" clearable v-if="query">
    </el-input>
    <el-button type="info" @click="$emit('query')" v-if="query">查找</el-button>
    <el-button type="primary" plain @click="$emit('refresh')" v-if="refresh">刷新</el-button>
  </div>
</template>

<script>
export default {
  name: "ToolBar",
  props: {
    chooseNum: Boolean,
    chooseDate: Boolean,
    query: Boolean,
    back: Boolean,
    refresh: Boolean,
    toolbar: {
      showNums: Number,
      queryStartDate: Date,
      queryEndDate: Date,
      queryStr: String
    }
  },
  data() {
    return {
      numOptions: [
        {label: '查看近20条', value: 20},
        {label: '查看近50条', value: 50},
        {label: '查看近100条', value: 100},
        {label: '查看近500条', value: 500},
        {label: '查看全部', value: -1}
      ]
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

  .choose-num {
    flex-shrink: 0;
    flex-basis: 160px;
  }

  .choose-date {
    flex-basis: 300px;
  }

  .input-query {
    flex-basis: 300px;
  }
}

</style>
