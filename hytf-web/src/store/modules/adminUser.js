import { login as apiLogin } from '@/api/adminAuth'
import { setAdminToken, removeAdminToken } from '@/utils/auth'

export default {
  namespaced: true,
  state: { token: '', info: {} },
  mutations: {
    SET_TOKEN(s, t) { s.token = t },
    SET_INFO(s, i) { s.info = i || {} }
  },
  actions: {
    async login({ commit }, payload) {
      const { data } = await apiLogin(payload)
      if (data.code !== 0) throw new Error(data.msg || '登录失败')
      setAdminToken(data.data.access_token)
      commit('SET_TOKEN', data.data.access_token)
      commit('SET_INFO', data.data)
      return data.data
    },
    logout({ commit }) {
      removeAdminToken()
      commit('SET_TOKEN', ''); commit('SET_INFO', {})
    }
  }
}