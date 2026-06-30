<template>
  <view class="mine-page">
    <view class="profile-card">
      <view class="profile-main">
        <view class="avatar" :style="{ background: avatarColor }">{{ avatarText }}</view>
        <view class="profile-info">
          <text class="name">{{ userInfo.real_name || userInfo.username }}</text>
          <text class="dept">{{ userInfo.dept || 'Base Room 员工' }}</text>
        </view>
      </view>
      <view class="profile-extra">
        <view class="extra-item">
          <text class="extra-num">12</text>
          <text class="extra-label">待办</text>
        </view>
        <view class="extra-item">
          <text class="extra-num">8</text>
          <text class="extra-label">已审批</text>
        </view>
        <view class="extra-item">
          <text class="extra-num">5</text>
          <text class="extra-label">客户</text>
        </view>
      </view>
    </view>

    <view class="menu-card">
      <view class="menu-item" v-for="(item, i) in menus" :key="i" @click="handle(item)">
        <view class="menu-left">
          <text class="menu-icon" :style="{ background: item.bg }">{{ item.icon }}</text>
          <text class="menu-label">{{ item.label }}</text>
        </view>
        <text class="menu-arrow">›</text>
      </view>
    </view>

    <button class="logout-btn" @click="logout">退出登录</button>
  </view>
</template>

<script>
export default {
  computed: {
    userInfo() { return this.$store.state.user.userInfo },
    avatarText() {
      const name = this.userInfo.real_name || this.userInfo.username || 'A'
      return name.slice(0, 1).toUpperCase()
    },
    avatarColor() {
      const colors = ['#4facfe', '#43e97b', '#fa709a', '#f6d365', '#a18cd1']
      const idx = (this.userInfo.username || '').length % colors.length
      return colors[idx] || '#4facfe'
    },
    menus() {
      return [
        { label: '首页应用管理', icon: '⚙️', bg: '#e0f7fa', path: '/pages/module-settings/module-settings' },
        { label: '我的审批', icon: '✅', bg: '#e8f5e9', path: '/pages/oa/approval' },
        { label: '考勤记录', icon: '⏰', bg: '#fff3e0', path: '/pages/oa/attendance' },
        { label: '系统设置', icon: '🔧', bg: '#f3e5f5', path: '' },
        { label: '关于我们', icon: 'ℹ️', bg: '#eceff1', path: '' }
      ]
    }
  },
  methods: {
    handle(item) {
      if (item.path) uni.navigateTo({ url: item.path })
      else uni.showToast({ title: '功能开发中', icon: 'none' })
    },
    logout() {
      uni.showModal({
        title: '提示',
        content: '确认退出登录？',
        success: res => {
          if (res.confirm) {
            this.$store.commit('user/LOGOUT')
            uni.reLaunch({ url: '/pages/login/login' })
          }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.mine-page { min-height: 100vh; background: #f5f7fa; padding: 24rpx 32rpx 40rpx; }

.profile-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-radius: 28rpx;
  padding: 40rpx;
  color: #fff;
  margin-bottom: 24rpx;
  box-shadow: 0 16rpx 40rpx rgba(79, 172, 254, 0.25);
}
.profile-main { display: flex; align-items: center; margin-bottom: 36rpx; }
.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48rpx;
  font-weight: 700;
  margin-right: 28rpx;
  background: rgba(255, 255, 255, 0.25);
}
.profile-info { flex: 1; }
.name { font-size: 40rpx; font-weight: 700; display: block; }
.dept { font-size: 26rpx; opacity: 0.9; margin-top: 8rpx; display: block; }

.profile-extra {
  display: flex;
  justify-content: space-around;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16rpx;
  padding: 20rpx 0;
}
.extra-item { text-align: center; }
.extra-num { font-size: 36rpx; font-weight: 700; display: block; }
.extra-label { font-size: 22rpx; opacity: 0.85; margin-top: 4rpx; display: block; }

.menu-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 0 28rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
  margin-bottom: 24rpx;
}
.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28rpx 0;
  border-bottom: 1rpx solid #f2f3f5;
  &:last-child { border-bottom: none; }
}
.menu-left { display: flex; align-items: center; }
.menu-icon {
  width: 56rpx;
  height: 56rpx;
  border-radius: 14rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30rpx;
  margin-right: 20rpx;
}
.menu-label { font-size: 30rpx; color: #303133; }
.menu-arrow { font-size: 36rpx; color: #c0c4cc; }

.logout-btn {
  height: 92rpx;
  line-height: 92rpx;
  border-radius: 46rpx;
  background: #fff;
  color: #fa709a;
  font-size: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.04);
}
.logout-btn::after { border: none; }
</style>
