import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import router from './router'
import store from './store'
import './permission'
import './styles/index.scss'
import { installSecurity } from './utils/security'

Vue.use(ElementUI, { size: 'small' })
Vue.config.productionTip = false

if (process.env.VUE_APP_ENABLE_SECURITY === 'true') installSecurity()

new Vue({ router, store, render: h => h(App) }).$mount('#app')