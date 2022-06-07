<template>
  <div class="app-container">

    <div id="new-item">
      <el-button size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleModify()">验证区块链</el-button>
    </div>

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
      <el-table-column label="当前区块hash">
        <template slot-scope="scope">
          {{ scope.row.cur_hash }}
        </template>
      </el-table-column>
      <el-table-column label="前一个区块hash">
        <template slot-scope="scope">
          {{ scope.row.pre_hash }}
        </template>
      </el-table-column>
      <el-table-column label="时间戳">
        <template slot-scope="scope">
          {{ scope.row.timestamp }}
        </template>
      </el-table-column>
      <el-table-column label="工作量证明">
        <template slot-scope="scope">
          {{ scope.row.nonce }}
        </template>
      </el-table-column>
      <el-table-column label="区块数据路径">
        <template slot-scope="scope">
          {{ scope.row.data_path }}
        </template>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import {getBlocks, verifyChain} from "@/api/blockchain";


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
      getBlocks(this.$route.query.user_id).then(response => {
        this.list = response
        this.listLoading = false
      })
    },

    handleModify(index, row) {
      this.listLoading = true
      verifyChain().then(res => {
        if (res.code == 0) this.$message.success(res.msg)
        else if (res.code == 1) this.$message.error(res.msg)
      })
      this.listLoading = false
    },

  }
}
</script>
