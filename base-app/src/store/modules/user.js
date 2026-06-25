export default {
  namespaced: true,
  state: {
    token: uni.getStorageSync('base_token') || '',
    userInfo: uni.getStorageSync('base_user') ? JSON.parse(uni.getStorageSync('base_user')) : {}
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      uni.setStorageSync('base_token', token)
    },
    SET_USER(state, user) {
      state.userInfo = user
      uni.setStorageSync('base_user', JSON.stringify(user))
    },
    LOGOUT(state) {
      state.token = ''
      state.userInfo = {}
      uni.removeStorageSync('base_token')
      uni.removeStorageSync('base_user')
    }
  }
}
