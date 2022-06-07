<template>
  <div class="dashboard-container">
    <div class="dashboard-text animate__animated animate__backInLeft animate__delay-1.5s">欢迎使用基于加密技术的农产品溯源仿真系统</div>
    <PanelGroup/>

    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :lg="12">
        <el-card class="box-card">
          <PersonCountBar/>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :lg="12">
        <el-card class="box-card">
          <PersonCountPie/>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import PersonCountBar from "@/components/Charts/PersonCount";
import PersonCountPie from "@/components/Charts/PersonCountPie";
import PanelGroup from "./components/PanelGroup/index"

export default {
  name: 'Dashboard',
  components: {
    PersonCountBar,
    PersonCountPie,
    PanelGroup,
  },
  data() {
    return {
    }
  },
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 50px;
    line-height: 66px;
    text-align: center;
    letter-spacing: 5px;
    font-family: "Microsoft YaHei";
  }
}
</style>

