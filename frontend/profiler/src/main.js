import Vue from 'vue'
import App from './App.vue'
import hljs from 'highlight.js'

import 'bootswatch/dist/sketchy/bootstrap.min.css'

Vue.use(hljs.vuePlugin);

Vue.config.productionTip = false

new Vue({
  render: function (h) { return h(App) },
}).$mount('#app')
