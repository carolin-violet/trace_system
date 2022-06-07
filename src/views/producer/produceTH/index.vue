<template>
  <div class="app-container">

    <div id="new-item">
      <el-button size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleModify()">添加温湿度信息</el-button>
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
      <el-table-column label="时间">
        <template slot-scope="scope">
          {{ scope.row.time }}
        </template>
      </el-table-column>
      <el-table-column label="温度">
        <template slot-scope="scope">
          {{ scope.row.temp }}
        </template>
      </el-table-column>
      <el-table-column label="湿度">
        <template slot-scope="scope">
          {{ scope.row.hum }}
        </template>
      </el-table-column>
    </el-table>

    <!--    修改信息的界面-->
    <el-dialog :visible.sync="dialogFormVisible" width="30%">
      <el-form :model="info">
        <el-form-item label="用户id:" label-width="110">
          <el-input v-model="info.user_id" autocomplete="off" disabled></el-input>
        </el-form-item>
        <el-form-item label="生产区域:" label-width="110">
          <el-input v-model="info.area_id" autocomplete="off" disabled></el-input>
        </el-form-item>
        <el-form-item label="生产批次:" label-width="110">
          <el-input v-model="info.batch" autocomplete="off" disabled></el-input>
        </el-form-item>
        <el-form-item label="·温度:" label-width="110">
          <el-input v-model="info.temp" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="·湿度:" label-width="110">
          <el-input v-model="info.hum" autocomplete="off"></el-input>
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
import {getProduceTH, addProduceInfo, addProduceTH} from "@/api/produce";


export default {
  data() {
    return {
      list: null,
      listLoading: true,
      dialogFormVisible: false,
      info: null,
    }
  },
  created() {
    this.info = {
      user_id: this.$route.query.data.user_id,
      area_id: this.$route.query.data.area_id,
      batch: this.$route.query.data.batch,
      temp: '',
      hum: '',
    }
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getProduceTH(this.$route.query.data).then(response => {
        this.list = response
        this.listLoading = false
      })
    },

    handleModify(index, row) {
      this.dialogFormVisible = true
      const temp = {
        user_id: this.$route.query.data.user_id,
        area_id: this.$route.query.data.area_id,
        batch: this.$route.query.data.batch,
        temp: '',
        hum: '',
      }
    },

    Submit() {
      addProduceTH(this.info).then(res => {
        if (res.code == 0) {
          this.$message.success(res.msg)
          this.info.temp =  ''
          this.info.hum = ''
          this.dialogFormVisible = false
          this.fetchData()
        }
      })
    },

  }
}
</script>
