<template>
  <div class="instruction">
    <el-dialog title="使用说明编辑" :visible.sync="showInstructionInfoEditor" v-loading="dialogLoading">
      <InstructionInfoEditor :form="form" @editorCancel="editorCancel"
                             @editorConfirm="editorConfirm"></InstructionInfoEditor>
    </el-dialog>
    <div class="container">
      <div class="header">
        <Toolbar refresh @refresh="getInstructionList"></Toolbar>
        <el-button type="primary" plain @click="handleAdd">添加使用说明</el-button>
      </div>
      <el-table class="table" :data="slicedData" v-loading="tableLoading" @sort-change="changeSortType"
                :default-sort="{prop: 'noticeID', order: 'descending'}">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="instructionName" label="标题" width="250" :sortable="'custom'"></el-table-column>
        <el-table-column prop="instructionTags" label="标签" width="auto">
          <template slot-scope="scope">
            <el-tag v-for="tag in scope.row.instructionTags" :key="tag" type="success" disable-transitions>
              {{ tag }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="150">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" size="small" class="delete" @click="handleDelete(scope.row)">删除</el-button>
            <el-button type="text" size="small" class="lookup" @click="handleLookUp(scope.row)">编辑内容</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="pagination" layout="prev, pager, next" :page-size="pageSize"
                     :current-page.sync="currentPage" :total="dataLength" background>
      </el-pagination>
    </div>
  </div>
</template>

<script>
import Toolbar from '@/components/Toolbar'
import InstructionInfoEditor from '@/components/Editor/InstructionInfoEditor'

export default {
  name: "Instruction",
  components: {
    InstructionInfoEditor,
    Toolbar
  },
  data() {
    return {
      dialogLoading: false,
      tableLoading: false,
      instructionList: [
        /*
        {
          instructionName: '3D辉夜机使用说明',
          instructionID: 1,
          instructionTags: ['快乐', '好用'],
          instructionCoverURL: null
        }
        */
      ],
      sortType: {
        prop: 'instructionID',
        order: 'descending'
      },
      pageSize: 10,
      currentPage: 1,
      showInstructionInfoEditor: false,
      form: {
        instructionID: null,
        instructionName: '',
        instructionTags: [],
        instructionCoverURL: null
      }
    }
  },
  computed: {
    dataLength() {
      return this.instructionList.length
    },
    slicedData() {
      this.doSort()
      return this.instructionList.slice(this.pageSize * (this.currentPage - 1),
          this.pageSize * this.currentPage <= this.instructionList.length ?
              this.pageSize * this.currentPage : this.instructionList.length)
    }
  },
  mounted() {
    this.getInstructionList()
  },
  methods: {
    changeSortType(event) {
      if (event) {
        this.sortType.prop = event.prop
        this.sortType.order = event.order
      }
      if (!this.sortType.order) {
        this.sortType.prop = 'instructionID'
        this.sortType.order = 'descending'
      }
    },
    doSort() {
      this.$utils.sort(this.instructionList, this.sortType, 'instructionID')
    },
    getInstructionList() {
      this.tableLoading = true
      this.$api.instruction.getInstructionList().then((res) => {
        if (res.data.errCode === 0) {
          this.instructionList = res.data.instructionList
          this.$utils.alertMessage(this, '获取数据成功', 'success')
        } else {
          this.$utils.error.APIError(this, res.data)
        }
        this.tableLoading = false
      }).catch((err) => {
        this.$utils.error.ServerError(this, err)
        this.tableLoading = false
      })
    },
    handleAdd() {
      if (this.form.instructionID) {
        this.form = {
          instructionID: null,
          instructionName: '',
          instructionTags: [],
          instructionCoverURL: null
        }
      }
      this.showInstructionInfoEditor = true
    },
    handleEdit(row) {
      this.form = {
        instructionID: row.instructionID,
        instructionName: row.instructionName,
        instructionTags: row.instructionTags.concat(),
        instructionCoverURL: row.instructionCoverURL
      }
      this.showInstructionInfoEditor = true
    },
    handleDelete(row) {
      this.$confirm('此操作将删除该使用说明, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.tableLoading = true
        this.$api.instruction.deleteInstruction({instructionID: row.instructionID}).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '删除成功', 'success')
            this.getInstructionList()
          } else {
            this.$utils.error.APIError(this, res.data)
            this.tableLoading = false
          }
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.tableLoading = false
        })
      }).catch(() => {
      })
    },
    handleLookUp(row) {
      this.$router.push({
        name: 'InstructionEditor',
        query: {
          instructionID: row.instructionID
        }
      })
    },
    editorCancel() {
      this.showInstructionInfoEditor = false
    },
    editorConfirm() {
      this.dialogLoading = true
      // 创建
      if (!this.form.instructionID) {
        let formData = new FormData()
        formData.append('instructionName', this.form.instructionName)
        formData.append('instructionTags', this.form.instructionTags)
        formData.append('instructionCover', this.form.instructionCoverURL)
        this.$api.instruction.addInstruction(formData).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '添加成功', 'success')
            this.form = {
              instructionID: null,
              instructionName: '',
              instructionTags: [],
              instructionCoverURL: null
            }
            this.getInstructionList()
          } else {
            this.$utils.error.APIError(this, res.data)
          }
          this.dialogLoading = false
          this.showInstructionInfoEditor = false
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.dialogLoading = false
          this.showInstructionInfoEditor = false
        })
      }
      // 编辑
      else {
        let formData = new FormData()
        formData.append('instructionID', this.form.instructionID)
        formData.append('instructionName', this.form.instructionName)
        formData.append('instructionTags', this.form.instructionTags)
        if (typeof this.form.instructionCoverURL === "object") {
          formData.append('instructionCover', this.form.instructionCoverURL)
        }
        this.$api.instruction.updateInstruction(formData).then((res) => {
          if (res.data.errCode === 0) {
            this.$utils.alertMessage(this, '编辑成功', 'success')
            this.getInstructionList()
          } else {
            this.$utils.error.APIError(this, res.data)
          }
          this.dialogLoading = false
          this.showInstructionInfoEditor = false
        }).catch((err) => {
          this.$utils.error.ServerError(this, err)
          this.dialogLoading = false
          this.showInstructionInfoEditor = false
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

.pagination {
  margin-top: $--pagination-margin-top;
  margin-bottom: $--pagination-margin-bottom;
}

.delete {
  color: $--color-danger;

  &:focus, &:hover {
    color: mix($--color-danger, $--color-white, 75%);
  }

  &:active {
    color: mix($--color-danger, $--color-black, 75%);
  }
}

.lookup {
  color: $--color-lookup;

  &:focus, &:hover {
    color: mix($--color-lookup, $--color-white, 75%);
  }

  &:active {
    color: mix($--color-lookup, $--color-black, 75%);
  }
}
</style>

<style lang="scss">
.el-tag + .el-tag {
  margin-left: 5px;
}
</style>
