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
      <el-table-column label="生产商id">
        <template slot-scope="scope">
          {{ scope.row.producer_id }}
        </template>
      </el-table-column>
      <el-table-column label="种植区域">
        <template slot-scope="scope">
          {{ scope.row.area_id }}
        </template>
      </el-table-column>
      <el-table-column label="种植批次">
        <template slot-scope="scope">
          {{ scope.row.batch }}
        </template>
      </el-table-column>
      <el-table-column label="商品名称">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column label="商品重量">
        <template slot-scope="scope">
          {{ scope.row.weight }}
        </template>
      </el-table-column>
      <el-table-column label="物流id">
        <template slot-scope="scope">
          {{ scope.row.logistics_id }}
        </template>
      </el-table-column>
      <el-table-column label="始发地">
        <template slot-scope="scope">
          {{ scope.row.ini }}
        </template>
      </el-table-column>
      <el-table-column label="目的地">
        <template slot-scope="scope">
          {{ scope.row.des }}
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="primary" @click="getQRCODE(scope.$index, scope.row)">获取二维码</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!--    添加商品信息的界面-->
    <el-dialog :visible.sync="dialogFormVisible" width="50%">
      <img :src="imgUrl" alt="">
    </el-dialog>

  </div>
</template>

<script>
import {getCommodities, getImg} from "@/api/sale";


export default {
  data() {
    return {
      list: null,
      listLoading: true,
      dialogFormVisible: false,
      imgUrl: null
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getCommodities(this.$route.query.user_id || this.$store.getters.user_id).then(response => {
        console.log(response);
        this.list = response
        this.listLoading = false
      })
    },

    getQRCODE(index, row) {
      getImg(row.logistics_id).then(res => {
        this.imgUrl = URL.createObjectURL(res)
        this.dialogFormVisible = true
      })
    },

  },
}

</script>
