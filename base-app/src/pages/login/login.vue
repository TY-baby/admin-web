<template>
  <view class="login-page">
    <view class="logo">Base Room</view>
    <view class="form">
      <input v-model="form.username" placeholder="用户名" class="input" />
      <input v-model="form.password" placeholder="密码" password class="input" />
      <button type="primary" @click="login" :loading="loading">登录</button>
    </view>
  </view>
</template>

<script>
import { login } from '../../api/auth'

export default {
  data() {
    return {
      loading: false,
      form: { username: 'admin', password: '123456' }
    }
  },
  methods: {
    async login() {
      this.loading = true
      const res = await login(this.form)
      this.loading = false
      if (res.code === 0) {
        this.$store.commit('user/SET_TOKEN', res.data.token)
        this.$store.commit('user/SET_USER', res.data.userInfo)
        uni.switchTab({ url: '/pages/index/index' })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.login-page { min-height: 100vh; background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); display: flex; flex-direction: column; align-items: center; padding-top: 180rpx; }
.logo { font-size: 56rpx; color: #fff; font-weight: bold; margin-bottom: 80rpx; }
.form { width: 80%; background: #fff; border-radius: 16rpx; padding: 40rpx; }
.input { height: 80rpx; border-bottom: 1rpx solid #eee; margin-bottom: 24rpx; padding: 0 16rpx; }
</style>
