import Vue from 'vue'
//导入路由
import Router from 'vue-router'
//导入登录页
import Login from '../views/Login'
import Home from "../views/Home";
//使用路由
Vue.use(Router);

export default new Router({
  routes:[
    //登錄頁
    {
      //通过/login访问
      path:'/',

      name:'Login',
      component:Login
    },
    {
      path:'/home',
      name:"Home",
      component:Home
    },

  ]
})
