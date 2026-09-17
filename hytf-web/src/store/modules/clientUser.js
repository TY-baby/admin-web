import { login as apiLogin } from '@/api/clientAuth'
import { getAccounts } from '@/api/clientHome'
import { setClientToken, removeClientToken } from '@/utils/auth'

export default {
  namespaced: true,
  state: { token: '', info: {}, accounts: [], currentAccount: null },
  mutations: {
    SET_TOKEN(s, t) { s.token = t },
    SET_INFO(s, i) { s.info = i || {} },
    SET_ACCOUNTS(s, list) {
      s.accounts = list || []
      if (!s.currentAccount && list && list.length) s.currentAccount = list[0]
    },
    SET_CURRENT(s, acc) { s.currentAccount = acc }
  },
  actions: {
    async login({ commit }, payload) {
      const { data } = await apiLogin(payload)
      if (data.code !== 0) throw new Error(data.msg || '鐧诲綍澶辫触')
      setClientToken(data.data.access_token)
      commit('SET_TOKEN', data.data.access_token)
      commit('SET_INFO', data.data)
      return data.data
    },
    async loadAccounts({ commit }) {
      const { data } = await getAccounts()
      if (data.code === 0) commit('SET_ACCOUNTS', data.data || [])
      return data.data
    },
    logout({ commit }) {
      removeClientToken()
      commit('SET_TOKEN', ''); commit('SET_INFO', {})
      commit('SET_ACCOUNTS', []); commit('SET_CURRENT', null)
    }
  }
}