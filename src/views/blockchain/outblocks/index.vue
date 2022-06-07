<template>
  <div class="app-container">

    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="ID" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="物流id">
        <template slot-scope="scope">
          {{ scope.row.logistics_id }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="600" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleModify(scope.$index, scope.row)">加入区块链</el-button>
       </template>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import {getOutBlocks, addBlock} from "@/api/blockchain";


export default {
  data() {
    return {
      list: null,
      listLoading: true,
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getOutBlocks(this.$route.query.user_id).then(response => {
        this.list = response
        this.listLoading = false
      })
    },

    handleModify(index, row) {
      const data = {
        "logistics_id": row.logistics_id
      }
      addBlock(data).then(res => {
        if (res.code == 0) {
          this.$message.success(res.msg)
          this.fetchData()
        }
      }).catch(err => this.$message.error(err))
    },

  }
}
</script>
