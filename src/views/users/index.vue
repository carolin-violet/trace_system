<template>
  <div class="app-container">

    <div id="new-item">
      <el-button size="mini" type="primary" icon="el-icon-circle-plus-outline" @click="handleModify()">添加用户</el-button>
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
      <el-table-column label="用户id">
        <template slot-scope="scope">
          {{ scope.row.user_id }}
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="用户角色" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.role | rolesFilter">{{ scope.row.role }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="姓名" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="联系电话" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.tel }}
        </template>
      </el-table-column>
      <el-table-column label="密码" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.password }}
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="性别" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.gender | statusFilter">{{ scope.row.gender }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="600" align="center">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="handleModify(scope.$index, scope.row)">修改信息</el-button>
          <el-button size="mini " type="danger" @click="handleDelete(scope.$index, scope.row)">删除用户</el-button>
        </template>
      </el-table-column>
    </el-table>


    <!--    修改信息的界面-->
    <el-dialog :visible.sync="dialogFormVisible" width="30%">
      <el-form :model="temp">
        <el-form-item v-show="temp.user_id" label="用户id:" label-width="110">
          <el-input v-model="temp.user_id" autocomplete="off" disabled></el-input>
        </el-form-item>
        <el-form-item label="用户类型:" label-width="110">
          <el-select v-model="temp.role" placeholder="请选择用户类型">
            <el-option label="生产者" value="producer"></el-option>
            <el-option label="运输者" value="transporter"></el-option>
            <el-option label="销售者" value="saler"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="姓名:" label-width="110">
          <el-input v-model="temp.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码:" label-width="110">
          <el-input v-model="temp.password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="联系电话:" label-width="110">
          <el-input v-model="temp.tel" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="性别:" label-width="110">
          <el-radio-group v-model="temp.gender">
            <el-radio label="男" value="male"></el-radio>
            <el-radio label="女" value="female"></el-radio>
          </el-radio-group>
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
import {getUsers,addUser, modifyUser, delUser} from "@/api/userInfo";

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        女: 'success',
        男: 'gray',
      }
      return statusMap[status]
    },
    rolesFilter(roles) {
      const rolesMap = {
        admin: 'danger',
        producer: 'success',
        transporter: 'info',
        saler: 'gray',
      }
      return rolesMap[roles]
    }
  },
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
      getUsers('all').then(response => {
        this.list = response
        this.listLoading = false
      })
    },

    handleModify(index, row) {
      this.dialogFormVisible = !this.dialogFormVisible
      if (row) {  // 点击的是修改按钮
        this.temp = row
      } else if (row === undefined) {  // 点击的是添加用户按钮
        this.temp = {
          role: '',
          name: '',
          tel: '',
          password: '',
          gender: '',
        }
      }
    },

    handleDelete(index, row) {
      this.$confirm('确定删除此用户?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        delUser(row.user_id).then(res => {
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
      if (this.temp.user_id === undefined) { // 添加用户
        addUser(this.temp).then(res => {
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
      } else { // 修改信息
        modifyUser(this.temp).then(res => {
          if (res.code == 0) {
            this.$message({
              message: res.msg,
              type: 'success',
              duration: 500
            })
            this.temp = ''
            this.dialogFormVisible = false
          }
        })
      }
    },

  }
}
</script>
