<template>
  <div>

    <section id="upload-form">
      <el-form ref="temp" :model="temp" label-width="80">
        <el-form-item label="用户id">
          <el-input v-model="temp.user_id" disabled></el-input>
        </el-form-item>
        <el-form-item label="区域">
          <el-input v-model="temp.area_id" placeholder="例如1、2、3"></el-input>
        </el-form-item>
        <el-form-item label="批次">
          <el-input v-model="temp.batch" placeholder="例如1、2、3"></el-input>
        </el-form-item>
        <el-form-item label="操作类型">
          <el-select v-model="temp.op_type" placeholder="请选择操作类型">
            <el-option label="播种" value="播种"></el-option>
            <el-option label="浇水" value="浇水"></el-option>
            <el-option label="施肥" value="施肥"></el-option>
            <el-option label="除虫" value="除虫"></el-option>
            <el-option label="除草" value="除草"></el-option>
            <el-option label="收割" value="收割"></el-option>
            <el-option label="存储" value="存储"></el-option>
            <el-option label="出库" value="出库"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label-width="150">
          <el-upload
            class="avatar-uploader"
            action=""
            :auto-upload="false"
            :show-file-list="false"
            :on-change="onChange">
            <img v-if="temp.img" :src="temp.img" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
        </el-form-item>
        <el-form-item label="详情描述">
          <el-input type="textarea" v-model="temp.description" :autosize="{ minRows: 4, maxRows: 6}"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="success" @click="upload">上传</el-button>
        </el-form-item>
      </el-form>

    </section>

  </div>
</template>

<script>
import {addProduceInfo} from "@/api/produce";

export default {
  data() {
    return {
      temp: null
    };
  },
  created() {
    this.temp = this.$route.query.data
  },
  methods: {
    upload() {
      addProduceInfo(this.temp).then(res => {
        if (res.code == 0) {
          this.$message.success(res.msg)
          this.temp.area_id = this.$route.query.data.area_id
          this.temp.batch = this.$route.query.data.batch
          this.temp.op_type = null
          this.temp.img = null
          this.temp.description = null
        }
      })
    },
    onChange(file){
      if (file) {
        const testmsg = /^image\/(jpeg|png|jpg)$/.test(file.raw.type)
        const isLt5M = file.size / 1024 / 1024 < 5;
        if (!testmsg) {
          this.$message.error('上传头像图片只能是 JPG/PNG 格式!');
          return false
        }
        if (!isLt5M) {
          this.$message.error('上传头像图片大小不能超过 5MB!');
          return false
        }

        const reader = new FileReader();
        reader.readAsDataURL(file.raw)
        reader.onload = e => {
          this.temp.img = e.target.result;
        }
      }
    },
  }
}
</script>

<style scoped lang="scss">
#upload-form{
  margin: 100px auto;
  width: 400px;
  height: auto;

  .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    &:hover{
      border-color: #409EFF;
    }
    .avatar-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 178px;
      height: 178px;
      line-height: 178px;
      text-align: center;
      border: 1px dashed #d9d9d9;
    }
    .avatar {
      width: 178px;
      height: 178px;
      display: block;
      border: 1px dashed #d9d9d9;
    }

  }
}

</style>
