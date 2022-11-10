<template>
  <div id="building">
        <div class="login_title">
          <h2>医疗记录系统</h2>
          <h2>Medical Records System</h2>
        </div>

    <el-tabs type="border-card" style="width: 90%;margin: auto">
      <el-tab-pane label="创建记录">

        <el-form  :model="form" label-width="80px" style="width: 95%;margin: auto" :rules="formRules" ref="formRules" prop="form">
          <el-form-item label="患者姓名" prop="PatientName">
            <el-input v-model="form.PatientName" ></el-input>
          </el-form-item>
          <el-form-item label="住院时间" >
            <el-col :span="11">
              <el-form-item label="" prop="In_time" >
              <el-date-picker type="date" placeholder="选择日期" v-model="form.In_time" style="width: 100%;" ></el-date-picker>
                </el-form-item>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11">
              <el-form-item label="" prop="Out_time" >
              <el-date-picker type="date" placeholder="选择日期" v-model="form.Out_time" style="width: 100%;" ></el-date-picker>
              </el-form-item>
            </el-col>
          </el-form-item>
          <el-form-item label="费用" prop="Fee">
            <el-input v-model="form.Fee" ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit" :disabled="this.GLOBAL.userAuth !== 1 ">创建</el-button>
          </el-form-item>
        </el-form>


      </el-tab-pane>

      <el-tab-pane label="记录搜索">


          <el-form style="width: 95%;margin: auto">
            <el-form-item lable="搜索" >
            <el-col :span="15">
              <el-form-item label="">
                <el-input v-model="info" placeholder="请输入信息"></el-input>
              </el-form-item>
            </el-col>

              <el-col :span="5">
          <el-form-item label="">
          <el-select v-model="value" placeholder="请选择信息类型">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
                </el-option>
              </el-select>
          </el-form-item>
                </el-col>

              <el-col :span="3">
                <el-button type="primary" @click="search">搜索</el-button>
              </el-col>

            </el-form-item>


          </el-form>

        <el-table
          :data="tableData"
          height="400"
          border
          style="width: 100%">
          <el-table-column
            prop="PatientName"
            label="患者姓名"
           >
          </el-table-column>
          <el-table-column
            prop="In_time"
            label="入院时间"
            >
          </el-table-column>
          <el-table-column
            prop="Out_time"
            label="出院时间">
          </el-table-column>
          <el-table-column
            prop="Fee"
            label="费用">
          </el-table-column>
          <el-table-column
            prop="RecordId"
            label="记录编号">
          </el-table-column>
        </el-table>





      </el-tab-pane>

    </el-tabs>

  </div>

</template>

<script>
export default {
  data() {
    return {
      form: {
        PatientName: '',
        In_time: '',
        Out_time: '',
        Fee: ''
      },
      formRules: {
        PatientName: [{
          required: true,
          message: "请输入患者姓名",
          trigger: "blur"
        },
          {
            min: 3,
            max: 18,
            message: "长度在 3 到 18 个字符",
            trigger: "blur",
          },
        ],
        In_time: [{
          required: true,
          message: "请输入入院时间",
          trigger: "blur"
        },
        ],
        Out_time: [{
          required: true,
          message: "请输入出院时间",
          trigger: "blur"
        },

        ],
        Fee: [{
          required: true,
          message: "请输入费用",
          trigger: "blur"
        },
        ]
      },
      options: [{
        value: '1',
        label: '患者姓名'
      }, {
        value: '2',
        label: '就医记录ID'
      }, ],
      value: '',
      info:'',
      searchForm:{
        Info:'',
        Method:''
      },
      tableData: [],

      recordInfo:{
        PatientName: '',
        In_time: '',
        Out_time: '',
        Fee: '',
        RecordId:''
      },





    }
  },
  methods: {
    onSubmit() {
      this.$refs.formRules.validate((valid) => {
        const startDate = this.form.In_time
        const endDate = this.form.Out_time
        const startTime = new Date(startDate).getTime()
        const endTime = new Date(endDate).getTime()

        if (!valid) return;
        if ( endTime < startTime) {
          this.$message.error('结束日期必须大于开始日期，请重新选择！')
          return;
        }
        this.$axios.post("/api/sendtx", this.qs.stringify(this.form)).then((
          res) => {
          console.log(res)
          if (res.data.message === 'success send the record') {
            this.$message.success("记录 id 为"+res.data.recordId);
          }
          else{
            this.$message.error("创建失败，请重试");
          }
        })
      })
    },
    search(){
      this.searchForm.Info = this.info
      this.searchForm.Method = this.value
      this.$axios.post("/api/query", this.qs.stringify(this.searchForm)).then((
        res) => {
        console.log(res)
        if (res.data.message === 'successful') {
          this.tableData = res.data.record;
        }
        else{
          this.$message.error("搜索失败");
        }
      })
    }
  }
}

</script>

<style scoped>
.login_title {
  /* 字体水平左右居中 */
  text-align:center;
}

.login_context {
  /* 宽度 */
  width: 450px;
  /* 高度 */
  height: 300px;
  /* 背景色 */
  background: #fff;
  /* 属性定位 */
  position: absolute;
  /* 属性定位，顶部占比 */
  top: 50%;
  /* 属性定位，左侧占比 */
  left: 50%;
  /* 水平垂直居中 */
  transform: translate(-50%, -50%);
  /* 四个角的圆角角度 */
  border-radius: 20px;
  /* 阴影 */
  box-shadow: 0 0 5px 2px #ddd;
}
#building{
  background:url("../assets/back2.jpeg");
  width:100%;
  height:100%;
  position:fixed;
  background-size:100% 100%;
}
</style>
