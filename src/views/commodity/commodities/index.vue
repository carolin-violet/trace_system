<template>
  <div class="app-container">

    <div id="new-item">
      <el-button size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleModify()">添加商品</el-button>
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
      <el-table-column label="生产者id">
        <template slot-scope="scope">
          {{ scope.row.producer_id }}
        </template>
      </el-table-column>
      <el-table-column label="商品名称">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="商品重量" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.weight }}</span>
        </template>
      </el-table-column>
      <el-table-column label="销售商id" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.saler_id }}
        </template>
      </el-table-column>
      <el-table-column label="物流单号" width="300" align="center">
        <template slot-scope="scope">
          {{ scope.row.logistics_id }}
        </template>
      </el-table-column>
      <el-table-column label="始发地" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.ini }}
        </template>
      </el-table-column>
      <el-table-column label="目的地" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.des }}
        </template>
      </el-table-column>
      <el-table-column label="商品详情信息地址" width="300" align="center">
        <template slot-scope="scope">
          {{ scope.row.qrcode_url }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="300" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handlegetDetail(scope.$index, scope.row)">查看物流</el-button>
          <el-button size="mini " type="danger" @click="handleDelete(scope.$index, scope.row)">删除商品</el-button>
        </template>
      </el-table-column>
    </el-table>


    <!--    添加商品信息的界面-->
    <el-dialog :visible.sync="dialogFormVisible" width="30%">
      <el-form :model="temp">
        <el-form-item label="生产商id:" label-width="110">
          <el-input v-model="temp.producer_id" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="生产区域:" label-width="110">
          <el-input v-model="temp.area_id" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="生产批次:" label-width="110">
          <el-input v-model="temp.batch" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="商品名字:" label-width="110">
          <el-input v-model="temp.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="商品重量:" label-width="110">
          <el-input v-model="temp.weight" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="销售商id:" label-width="110">
          <el-input v-model="temp.saler_id" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="始发地:" label-width="110">
          <el-input v-model="temp.ini" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="目的地:" label-width="110">
          <el-input v-model="temp.des" autocomplete="off"></el-input>
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
import {getCommodities, addCommodity, delCommodity} from "@/api/commodity";

export default {
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
      getCommodities().then(response => {
        this.list = response
        this.listLoading = false
      })
    },

    handleModify(index, row) {
      this.dialogFormVisible = !this.dialogFormVisible
      this.temp = {
        producer_id: this.$store.getters.user_id || null,
        area_id: '',
        batch: '',
        name: '',
        weight: '',
        saler_id: '',
        ini: '',
        des: '',
      }
    },

    handleDelete(index, row) {
      this.$confirm('确定删除此商品?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delCommodity(row.logistics_id).then(res => {
          if (res.code == 0) {
            this.$message({
              message: res.msg,
              type: 'success',
              duration: 500
            })
            this.fetchData()
          }
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },


    Submit() {
      addCommodity(this.temp).then(res => {
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

    handlegetDetail(index, row) {
      this.$router.push({
        path: '/commodity/logistics',
        query: {
          logistics_id: row.logistics_id
        }
      })
    }

  }
}
</script>
