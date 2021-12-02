import Vue from 'vue'
import App from '@/App.vue'
import '@/plugins/element'
import '@/plugins/mavonEditor'
import router from '@/router'
import store from '@/store'
import api from '@/api'
import utils from '@/utils'

Vue.config.productionTip = false

Vue.prototype.$api = api
Vue.prototype.$utils = utils

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
