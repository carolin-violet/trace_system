<template>
  <div id="person-count-bar" style="width: 100%;height: 50vh;" />
</template>

<script>
import {personCount} from "@/api/statistics";

export default {
  name: "PersonCountBar",
  data() {
    return {
      xData: null,
      yData: null,
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
      var myChart = echarts.init(document.getElementById('person-count-bar'))
      const colorArr = ['#E67A61','#6ED9AF','#7ECCEA','#9E81CE']
      // 配置参数
      var option = {
        // color: ['#E67A61','#6ED9AF','#7ECCEA','#9E81CE'],
        title: {
          text: '用户人数统计'
        },
        tooltip: {
          //trigger: 'axis',    //显示其他分类
          axisPointer: {
            // 坐标轴指示器，坐标轴触发有效
            type: "shadow", // 默认为直线，可选为：'line' | 'shadow'
          },
          formatter: function (params) {
            return (
              '<span style="font-size:10px">' +
              params.name +
              "<br/>" +
              params.marker +
              '<span style="color:' +
              params.color +
              ';font-size:10px;">' +
              params.value +
              "人" +
              "</span>" +
              "</span>"
            );
          },
        },
        legend: {
          top: "3%",
          right: "5%",
          icon: "pin",
          itemWidth: 13,
          itemHeight: 13, //图例宽高
          textStyle: {
            color: "#A0B2D3",
            fontSize: 20,
          },
        },
        grid: {
          left: "5%",
          right: "5%",
          bottom: "5%",
          containLabel: true,
        },
        xAxis: [{
          type: 'category',
          data: this.xData
        }],
        yAxis: [{
          type: 'value'
        }],
        // series: this.yData,
        series: [
          {
            type: 'bar',
            data: this.yData,
            itemStyle: {
              color: (arg) => {
                if (arg.name === '管理者') {
                  return colorArr[0]
                } else if (arg.name === '生产者') {
                  return colorArr[1]
                } else if (arg.name === '运输人员') {
                  return colorArr[2]
                } else if (arg.name === '销售商') {
                  return colorArr[3]
                }
              }
            }
          }
        ],
        animation: true,
        animationDuration: 4000
      }
      myChart.setOption(option)
    },

    //  获取数据
    getPersonCount() {
      personCount().then(res => {
        // this.yData = res.data.map((item, index) => {
        //   let obj = {
        //     name: item["name"],
        //     data: [],
        //     type: 'bar',
        //     barWidth: 20,
        //     barGap: 0.1,
        //   }
        //   for (let i = 0; i < res.data.length; i++) {
        //     if (index === i) {
        //       obj.data.push(item['value'])
        //     } else if (index !== i) {
        //       obj.data.push(0)
        //     }
        //   }
        //   return obj
        // })
        this.xData = res.data.map(item => item['name'])
        this.yData = res.data.map(item => item['value'])
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
