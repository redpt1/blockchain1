// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import VueRouter from 'vue-router';
import router from './router'
import axios from 'axios'
import qs from 'qs'
import global_ from './components/Global'//引用文件

Vue.prototype.GLOBAL = global_//挂载到Vue实例上面

Vue.prototype.$axios = axios    //全局注册，使用方法为:this.$axios
Vue.prototype.qs = qs   //全局注册，使用方法为:this.qs

Vue.use(VueRouter);
Vue.use(ElementUI);
Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  components: { App },
  router,
  template: '<App/>'
})
