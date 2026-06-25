import { login, getInfo } from '@/api/auth'

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('base_token') || '',
    userInfo: JSON.parse(localStorage.getItem('base_user') || '{}')
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('base_token', token)
    },
    SET_USER(state, user) {
      state.userInfo = user
      localStorage.setItem('base_user', JSON.stringify(user))
    },
    LOGOUT(state) {
      state.token = ''
      state.userInfo = {}
      localStorage.removeItem('base_token')
      localStorage.removeItem('base_user')
    }
  },
  actions: {
    async login({ commit }, form) {
      const data = await login(form)
      commit('SET_TOKEN', data.token)
      commit('SET_USER', data.userInfo)
      return data
    },
    async getInfo({ commit }) {
      const data = await getInfo()
      commit('SET_USER', data)
      return data
    },
    logout({ commit }) {
      commit('LOGOUT')
    }
  }
}
