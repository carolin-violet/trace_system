<template>
  <div id="person-count-pie" style="width: 100%;height: 50vh;" />
</template>

<script>
import {personCount} from "@/api/statistics";

export default {
  name: "PersonCountPie",
  data() {
    return {
      list: null,
    }
  },
  mounted() {
    this.getPersonCount()
  },
  methods:{
    // 创图表
    initChart() {
      var echarts = require('echarts')
      // 初始化echarts实例
      var myChart = echarts.init(document.getElementById('person-count-pie'))
      // 配置参数
      var option = {
        color: ['#E67A61','#6ED9AF','#7ECCEA','#9E81CE'],
        title: {
          text: '用户人数比例',
          subtext: 'Fake Data',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            label: {
              normal: {
                show: true,
                formatter: '{b}: {c}({d}%)' //自定义显示格式(b:name, c:value, d:百分比)
              }
            },
            data:this.list
          }
        ],
        animation: true,
        animationDuration: 4000
      };
      myChart.setOption(option)
    },

    //  获取数据
    getPersonCount() {
      personCount().then(res => {
        let count = 0
        res.data.forEach(item => count += item['value'])
        this.list = res.data
        this.initChart()
      })
    }
  }
}
</script>

<style scoped>
#main{
  margin: 0 auto;
}
</style>
