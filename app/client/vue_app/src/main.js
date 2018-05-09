import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import './filters'

// css
require('./assets/css/tachyons.css')
require('./assets/css/style.css')


Vue.config.productionTip = true

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
