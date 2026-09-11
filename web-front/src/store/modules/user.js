import { login, getInfo } from '@/api/auth'

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('my_token') || '',
    userInfo: JSON.parse(localStorage.getItem('my_user') || '{}')
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('my_token', token)
    },
    SET_USER(state, user) {
      state.userInfo = user
      localStorage.setItem('my_user', JSON.stringify(user))
    },
    LOGOUT(state) {
      state.token = ''
      state.userInfo = {}
      localStorage.removeItem('my_token')
      localStorage.removeItem('my_user')
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