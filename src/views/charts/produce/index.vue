<template>
  <div id="visualize-container">


  <el-date-picker v-model="time" align="right" type="date" placeholder="选择日期" :picker-options="pickerOptions" value-format="yyyy-MM-dd" style="margin:30px 0 0 100px">
  </el-date-picker>
  <el-button @click="getTHData" style="margin:30px 0 0 50px">
    获取温湿度信息
  </el-button>



      <div>
        <el-card class="box-card" id="temperature-count"  style="width: 90%;height: 50vh;margin: 30px auto" ></el-card>
        <el-card class="box-card" id="humidity-count"   style="width: 90%;height: 50vh;margin: 30px auto"></el-card>
      </div>

  </div>
</template>

<script>
import {getProduceTH} from "@/api/produce";

export default {
  name: "index",
  data() {
    return {
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        },
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            picker.$emit('pick', new Date());
          }
        }, {
          text: '昨天',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24);
            picker.$emit('pick', date);
          }
        }, {
          text: '一周前',
          onClick(picker) {
            const date = new Date();
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
            picker.$emit('pick', date);
          }
        }]
      },
      time: '',
      xData:null,
      y1:null,
      y2:null,
    }
  },
  mounted() {

  },
  methods:{
    // 创图表
    initChart() {
      var echarts = require('echarts')
      // 初始化echarts实例
      var myChart1 = echarts.init(document.getElementById('temperature-count'))
      // 配置参数
      var option1 = {
        color: '#6dfeb8',
        title: {
          text: '温度'
        },
        tooltip: {
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          data: this.xData
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} °C'
          }
        },
        series: [
          {
            data: this.y1,
            type: 'line',
            markPoint: {
              data: [{
                type: 'max',
                name: '最大值'
              }, {
                type: 'min',
                name: '最小值'
              }]
            }
          }
        ]
      };
      myChart1.setOption(option1)

      var myChart2 = echarts.init(document.getElementById('humidity-count'))
      // 配置参数
      var option2 = {
        color: '#6e7de8',
        title: {
          text: '湿度'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: this.xData
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value} %'
          }
        },
        series: [
          {
            data: this.y2,
            type: 'line',
            markPoint: {
              data: [{
                type: 'max',
                name: '最大值'
              }, {
                type: 'min',
                name: '最小值'
              }]
            }
          }
        ]
      };
      myChart2.setOption(option2)

    },

    getTHData() {
      if (this.$route.query.data.user_id){
        const data = {...this.$route.query.data, time:this.time}
        getProduceTH(data).then(res => {
          if (res.length) {
            this.$message.success('获取成功')
            this.xData = res.map(item => item.time)
            this.y1 = res.map(item => item.temp)
            this.y2 = res.map(item => item.hum)

            this.initChart()
          } else {
            this.$message.info('无当天温湿度信息')
          }
        }).catch(err => {
          this.$message.error(err)
        })
      }
    },


  },
}
</script>

<style scoped lang="scss">

</style>
