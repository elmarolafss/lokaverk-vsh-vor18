import Vue from 'vue'
import VueLazyload from 'vue-lazyload'
import App from './App.vue'
import router from './router'
import store from './store'

import './filters'

// css
require('./assets/css/tachyons.css')
require('./assets/css/style.css')

Vue.config.productionTip = true

Vue.use(VueLazyload, {
  preLoad: 1,
  error: 'dist/error.png',
  loading: './assets/loading.gif',
  attempt: 1,
  lazyComponent: true
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
