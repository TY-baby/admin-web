<template>
  <view class="login-page">
    <view class="login-top">
      <view class="login-wave">
        <svg viewBox="0 0 1440 320" preserveAspectRatio="none">
          <path fill="#ffffff" fill-opacity="1" d="M0,224L48,213.3C96,203,192,181,288,181.3C384,181,480,203,576,224C672,245,768,267,864,250.7C960,235,1056,181,1152,165.3C1248,149,1344,171,1392,181.3L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        </svg>
      </view>
      <view class="brand">
        <view class="logo-box">
          <text class="logo-icon">🌿</text>
        </view>
        <text class="brand-title">Base Room</text>
        <text class="brand-subtitle">移动办公 · 轻松高效</text>
      </view>
    </view>

    <view class="login-card">
      <text class="login-title">欢迎登录</text>
      <text class="login-desc">请输入账号密码进入工作台</text>

      <view class="input-group">
        <text class="input-label">账号</text>
        <view class="input-wrap">
          <text class="input-icon">👤</text>
          <input
            v-model="form.username"
            placeholder="请输入用户名"
            placeholder-style="color: #c0c4cc"
            class="input"
          />
        </view>
      </view>

      <view class="input-group">
        <text class="input-label">密码</text>
        <view class="input-wrap">
          <text class="input-icon">🔒</text>
          <input
            v-model="form.password"
            placeholder="请输入密码"
            password
            placeholder-style="color: #c0c4cc"
            class="input"
          />
        </view>
      </view>

      <button
        class="login-btn"
        :loading="loading"
        :disabled="loading"
        @click="login"
      >
        登 录
      </button>

      <view class="login-tips">
        <text>演示账号：admin / 123456</text>
      </view>
    </view>
  </view>
</template>

<script>
import { login } from '@/api/auth'

export default {
  data() {
    return {
      loading: false,
      form: { username: '', password: '' }
    }
  },
  onLoad() {
    // 已登录直接跳转
    if (this.$store.state.user.token) {
      uni.switchTab({ url: '/pages/index/index' })
    }
  },
  methods: {
    async login() {
      if (!this.form.username || !this.form.password) {
        return uni.showToast({ title: '请输入账号密码', icon: 'none' })
      }
      this.loading = true
      try {
        const res = await login(this.form)
        if (res.code === 0) {
          this.$store.commit('user/SET_TOKEN', res.data.token)
          this.$store.commit('user/SET_USER', res.data.userInfo)
          uni.showToast({ title: '登录成功', icon: 'success' })
          setTimeout(() => {
            uni.switchTab({ url: '/pages/index/index' })
          }, 500)
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #e0f7fa 0%, #f5f7fa 100%);
}

.login-top {
  position: relative;
  height: 45vh;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 120rpx;
  svg { width: 100%; height: 100%; }
}

.brand {
  text-align: center;
  color: #fff;
  z-index: 1;
}

.logo-box {
  width: 140rpx;
  height: 140rpx;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 36rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24rpx;
  backdrop-filter: blur(10rpx);
}

.logo-icon { font-size: 72rpx; }

.brand-title { font-size: 56rpx; font-weight: 700; display: block; letter-spacing: 2rpx; }
.brand-subtitle { font-size: 28rpx; opacity: 0.9; margin-top: 12rpx; display: block; }

.login-card {
  margin: -80rpx 40rpx 40rpx;
  background: #fff;
  border-radius: 32rpx;
  padding: 50rpx 40rpx;
  box-shadow: 0 20rpx 60rpx rgba(79, 172, 254, 0.12);
  position: relative;
  z-index: 2;
}

.login-title { font-size: 44rpx; font-weight: 700; color: #303133; display: block; }
.login-desc { font-size: 26rpx; color: #909399; margin: 12rpx 0 50rpx; display: block; }

.input-group { margin-bottom: 32rpx; }
.input-label { font-size: 26rpx; color: #606266; margin-bottom: 12rpx; display: block; }
.input-wrap {
  display: flex;
  align-items: center;
  background: #f5f7fa;
  border-radius: 16rpx;
  padding: 0 24rpx;
  height: 96rpx;
}
.input-icon { font-size: 32rpx; margin-right: 16rpx; }
.input {
  flex: 1;
  height: 96rpx;
  font-size: 30rpx;
  color: #303133;
}

.login-btn {
  margin-top: 20rpx;
  height: 96rpx;
  line-height: 96rpx;
  border-radius: 48rpx;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #fff;
  font-size: 32rpx;
  font-weight: 600;
  box-shadow: 0 12rpx 32rpx rgba(79, 172, 254, 0.35);
}
.login-btn::after { border: none; }

.login-tips {
  margin-top: 36rpx;
  text-align: center;
  font-size: 24rpx;
  color: #c0c4cc;
}
</style>
