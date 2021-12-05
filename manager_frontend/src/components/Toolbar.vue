<template>
  <div class="toolbar">
    <el-select class="choose-num" v-model="toolbar.showNums" placeholder="请选择" v-if="chooseNum"
               @change="$emit('query')">
      <el-option v-for="item in numOptions" :key="item.num"
                 :label="item.label" :value="item.num">
      </el-option>
    </el-select>
    <el-date-picker class="choose-date pointer" v-model="toolbar.queryStartDate" type="date" :editable="false"
                    placeholder="选择开始日期" v-if="chooseDate" @change="toolbar.queryEndDate && $emit('query')">
    </el-date-picker>
    <el-date-picker class="choose-date pointer" v-model="toolbar.queryEndDate" type="date" :editable="false"
                    placeholder="选择结束日期" v-if="chooseDate" @change="toolbar.queryStartDate && $emit('query')">
    </el-date-picker>
    <el-input class="input-query" placeholder="请输入查找内容" prefix-icon="el-icon-search"
              v-model="toolbar.queryStr" v-if="query" @keyup.enter.native="$emit('query')" clearable>
    </el-input>
    <el-button type="info" v-if="query" @click="$emit('query')">查找</el-button>
    <el-button type="primary" icon="el-icon-back" plain v-if="back" @click="$emit('back')"></el-button>
    <el-button type="primary" plain v-if="refresh" @click="$emit('refresh')">刷新</el-button>
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
  flex-shrink: 0;
  flex-basis: 160px;
}

.choose-date {
  flex-basis: 300px;
}

.input-query {
  flex-basis: 300px;
}

</style>
