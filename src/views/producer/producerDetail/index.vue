<template>
  <div class="app-container">

    <div id="new-item">
      <el-button size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleModify()">添加生产信息</el-button>
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
      <el-table-column label="操作方式">
        <template slot-scope="scope">
          {{ scope.row.op_type }}
        </template>
      </el-table-column>
      <el-table-column label="操作时间">
        <template slot-scope="scope">
          {{ scope.row.op_time }}
        </template>
      </el-table-column>
      <el-table-column label="描述">
        <template slot-scope="scope">
          {{ scope.row.description }}
        </template>
      </el-table-column>
      <el-table-column label="图片" width="180">
        <template slot-scope="scope">
          <el-image style="width: 100px; height: 100px" :src="scope.row.img " :preview-src-list="[scope.row.img]">
          </el-image>
        </template>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import {getProduceDetail} from "@/api/produce";


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
      getProduceDetail(this.$route.query.data).then(response => {
        this.list = response
        this.listLoading = false
      })
    },

    handleModify(index, row) {
      console.log(this.$route.query.data)
      const data = {
        user_id: this.$route.query.data.user_id,
        area_id: this.$route.query.data.area_id,
        batch: this.$route.query.data.batch,
        op_type: '',
        img: '',
        description: ''
      }
      this.$router.push({
        path: '/producer/uploadInfo',
        query: {
          data
        }
      })
    },


  }
}
</script>
