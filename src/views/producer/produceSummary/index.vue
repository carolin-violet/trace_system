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
      <el-table-column label="操作" width="600" align="center">
        <template slot-scope="scope">
          <el-button size="mini " type="success" @click="getDetail(scope.$index, scope.row)">查看生产信息详情</el-button>
          <el-button size="mini " type="info" @click="getTH(scope.$index, scope.row)">查看温湿度详情</el-button>
          <el-button size="mini " type="primary" @click="getCharts(scope.$index, scope.row)">查看统计图表</el-button>
        </template>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import {getProduceSummary} from "@/api/produce";


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
      getProduceSummary(this.$route.query.user_id || this.$store.getters.user_id).then(response => {
        this.list = response
        this.listLoading = false
      })
    },

    handleModify(index, row) {
        const temp = {
        user_id: this.$route.query.user_id || this.$store.getters.user_id,
        area_id: '',
        batch: '',
        op_type: '',
        img: '',
        description: ''
      }
      this.$router.push({
        path: '/producer/uploadInfo',
        query: {
          data: temp
        }
      })
    },


    getDetail(index, row) {
      this.$router.push({
        path: '/producer/producerDetail',
        query: {
          data: row
        }
      })
    },

    getTH(index, row) {
      this.$router.push({
        path: '/producer/produceTH',
        query: {
          data: row
        }
      })
    },

    getCharts(index, row) {
      this.$router.push({
        path: '/charts/produce',
        query: {
          data: row
        }
      })
    },

  }
}
</script>
