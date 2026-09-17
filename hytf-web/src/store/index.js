import Vue from 'vue'
import Vuex from 'vuex'
import clientUser from './modules/clientUser'
import adminUser from './modules/adminUser'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: { clientUser, adminUser }
})