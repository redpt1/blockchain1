<template>
  <div id="building">
  <div class="login">
    <div class="login_title">
      <h2>医疗记录系统</h2>
      <h2>Medical Records System</h2>
      <div class="login_context">

        <el-form :model="loginRuleForm" :rules="loginRules" ref="loginRules" class="login_box">

          <el-form-item label="账号" prop="userId">
            <el-input v-model="loginRuleForm.userId"></el-input>
          </el-form-item>

          <el-form-item label="密码" prop="passWord">
            <el-input type="password" v-model="loginRuleForm.passWord"></el-input>
          </el-form-item>

          <el-form-item class="btns">
            <el-button type="primary" @click="login">登录</el-button>
            <el-button @click="sign">注册</el-button>
          </el-form-item>

        </el-form>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
// Vue 代码逻辑
export default {
  data() {
    return {
      // 表单请求数据
      loginRuleForm: {
        userId: '',
        passWord: '',
      },
      // 表单验证规则
      loginRules: {
        userId: [{
          required: true,
          message: "请输入用户名",
          trigger: "blur"
        },
          {
            min: 3,
            max: 18,
            message: "长度在 3 到 18 个字符",
            trigger: "blur",
          },
        ],
        passWord: [{
          required: true,
          message: "请输入密码",
          trigger: "blur"
        },
          {
            min: 3,
            max: 18,
            message: "长度在 3 到 18 个字符",
            trigger: "blur",
          }
        ]
      }
    };
  },
  methods: {
    sign() {
      this.$refs.loginRules.validate((valid) => {
        if (!valid) return;
        this.$axios.post("/api/sign", this.qs.stringify(this.loginRuleForm)).then((
          res) => {
          console.log(res)

          if (res.data.message === 'successful') {// 跳转到主页
            this.$message.success("注册成功，请登录");
          }
          else{
            this.$message.error("注册失败，请重试");
          }
        })
      })
    },
    login() {
      this.$refs.loginRules.validate((valid) => {
        if (!valid) return;
        this.$axios.post("/api/login", this.qs.stringify(this.loginRuleForm)).then((
          res) => {
          console.log(res)
          if(res.data.message === "fail")
          {this.$message.error("登录失败，请检查用户名和密码");
            return;}
          if(res.data.authority === "doctor")
          {
            this.GLOBAL.userAuth = 1;
          }
          else
            this.GLOBAL.userAuth  = 0;

          this.$router.replace("/home"); //防止返回
          this.$message.success("您好, " + this.loginRuleForm.userId + " 欢迎进入医疗记录系统");

        })
      })
    }
  }
}
</script>

<style scoped>

.login {
  /* 高度 */
  height: 100%;
  /* 背景色 */
}

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
  /*box-shadow: 0 0 5px 2px #ddd;*/
}

.login_logo {
  /* 宽度 */
  width: 150px;
  /* 高度 */
  height: 150px;
  /* 属性定位 */
  position: absolute;
  /* 属性定位，顶部占比 */
  top: -75px;
  /* 属性定位，左侧占比 */
  left: 49%;
  /* logo左侧边距 */
  margin-left: -75px;
  /* 带有边框属性 */
  border: 1px solid #eee;
  /* 四个角的圆角角度 */
  border-radius: 50%;
  /* 背景色 */
  background: #fff;
  /* 设置内边距属性 */
  padding: 10px;
  /* 阴影 */
  box-shadow: 0 0 2px 2px #ddd;
}

.login_logo img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: rgb(238, 238, 238);
}

.login_box {
  width: 100%;
  position: absolute;
  bottom: 0;
  padding: 0 50px;
  /* 边框边距 */
  box-sizing: border-box;
}

.btns {
  /* 将对象作为弹性伸缩盒显示 */
  display: flex;
  /* 横轴方向上的对齐方式 */
  justify-content: flex-end;
}

#building{
  background:url("../assets/back.jpeg");
  width:100%;
  height:100%;
  position:fixed;
  background-size:100% 100%;
}

</style>
