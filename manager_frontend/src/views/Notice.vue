<template>
  <div class="notice">
    <div class="container">
      <div class="toolbar">
        <el-select v-model="showNums" placeholder="请选择">
          <el-option v-for="item in numOptions" :key="item.num"
                     :label="item.label" :value="item.num">
          </el-option>
        </el-select>
        <el-date-picker v-model="queryStartDate" type="date" :editable="false"
                        placeholder="选择开始日期" class="pointer">
        </el-date-picker>
        <el-date-picker v-model="queryEndDate" type="date" :editable="false"
                        placeholder="选择结束日期" class="pointer">
        </el-date-picker>
        <el-button type="primary" plain>新建公告</el-button>
      </div>
      <el-table class="table" :data="slicedData"
                :default-sort="{prop: 'noticeDate', order: 'descending'}" stripe>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="noticeDate" label="发布时间" width="150" sortable></el-table-column>
        <el-table-column prop="expireDate" label="过期时间" width="150" sortable></el-table-column>
        <el-table-column prop="noticeContent" label="概要" width="auto">
          <template slot-scope="scope">
            <el-scrollbar class="content">
              {{ scope.row.noticeContent }}
            </el-scrollbar>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" size="small" class="delete" @click="handleDelete(scope.row)"> 删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination layout="prev, pager, next" :page-size="pageSize" :current-page.sync="currentPage"
                     :total="dataLength" background>
      </el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  name: "Notice",
  data() {
    return {
      noticeData: [],
      pageSize: 10,
      currentPage: 1,
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
      ],
      showNums: 20,
      queryStartDate: '',
      queryEndDate: '',
      queryStr: ''
    }
  },
  computed: {
    dataLength() {
      return this.noticeData.length
    },
    slicedData() {
      return this.noticeData.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage < this.noticeData.length ?
              this.pageSize * this.currentPage : this.noticeData.length)
    }
  },
  mounted() {
    this.noticeData = [
      {
        noticeID: 1,
        noticeDate: '2021-11-24',
        expireDate: '2021-11-31',
        noticeContent: '大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！大家好！'
      },
      {
        noticeID: 2,
        noticeDate: '2021-11-25',
        expireDate: '2021-11-31'
      },
      {
        noticeID: 3,
        noticeDate: '2021-11-26',
        expireDate: '2021-11-30'
      },
    ]
  },
  methods: {
    handleEdit(row) {
      console.log(row)
    },
    handleDelete(row) {
      console.log(row)
    }
  }
}
</script>

<style scoped lang="scss">
@import "src/element-variables";

.toolbar {
  * {
    margin: 0 5px;
  }
}

.content {
  white-space: nowrap;
}

.table {
  margin: 10px auto 10px;
}

.delete {
  color: $--color-danger;

  &:focus, &:hover {
    color: mix($--color-danger, $--color-white, 75%);
  }

  &:active {
    color: $--color-danger;
  }
}

</style>