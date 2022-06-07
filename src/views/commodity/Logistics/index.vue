<template>
  <div class="app-container">

    <div id="new-item">
      <el-button size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleModify()">添加物流信息</el-button>
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
      <el-table-column label="运输者id">
        <template slot-scope="scope">
          {{ scope.row.transporter_id }}
        </template>
      </el-table-column>
      <el-table-column label="时间" width="250">
        <template slot-scope="scope">
          {{ scope.row.time }}
        </template>
      </el-table-column>
      <el-table-column label="当前所在地" width="250" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.cur }}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="状态" width="250" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
    </el-table>


    <!--    添加商品信息的界面-->
    <el-dialog :visible.sync="dialogFormVisible" width="30%">
      <el-form :model="temp">
        <el-form-item label="物流单号:" label-width="110">
          <el-input v-model="temp.logistics_id" autocomplete="off" disabled></el-input>
        </el-form-item>
        <el-form-item label="运输人员id:" label-width="110">
          <el-input v-model="temp.transporter_id" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="状态:" label-width="110">
          <el-select v-model="temp.status" placeholder="请选择操作类型">
            <el-option label="已发货" value="已发货"></el-option>
            <el-option label="运输中" value="运输中"></el-option>
            <el-option label="已到货" value="已到货"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="当前所在地:" label-width="110">
          <el-input v-model="temp.cur" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="Submit">确 定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import {getLogistics, addLogistics} from "@/api/logistics";


export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        已发货: 'info',
        运输中: 'gray',
        已到货: 'success',
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      listLoading: true,
      dialogFormVisible: false,
      temp: '',
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getLogistics(this.$route.query.logistics_id).then(response => {
        this.list = response
        this.listLoading = false
      })
    },

    handleModify(index, row) {
      this.dialogFormVisible = !this.dialogFormVisible
      this.temp = {
        logistics_id: this.$route.query.logistics_id,
        transporter_id: this.$store.getters.user_id || null,
        status: '',
        cur: '',
      }
    },


    Submit() {
      addLogistics(this.temp).then(res => {
        if (res.code == 0) {
          this.$message({
            message: res.msg,
            type: 'success',
            duration: 500
          })
          this.fetchData()
          this.temp = ''
          this.dialogFormVisible = false
        }
      })
    },


  }
}
</script>
