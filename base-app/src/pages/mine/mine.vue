<template>
  <view class="mine-page">
    <view class="profile">
      <view class="avatar">{{ avatarText }}</view>
      <view class="info">
        <text class="name">{{ userInfo.username }}</text>
        <text class="role">{{ userInfo.role }}</text>
      </view>
    </view>
    <view class="cells">
      <view class="cell">
        <text>我的客源</text>
        <text class="arrow">></text>
      </view>
      <view class="cell">
        <text>跟进记录</text>
        <text class="arrow">></text>
      </view>
      <view class="cell">
        <text>系统设置</text>
        <text class="arrow">></text>
      </view>
    </view>
    <button class="logout" type="warn" @click="logout">退出登录</button>
  </view>
</template>

<script>
export default {
  computed: {
    userInfo() { return this.$store.state.user.userInfo },
    avatarText() { return (this.userInfo.username || 'A').slice(0, 1).toUpperCase() }
  },
  methods: {
    logout() {
      uni.showModal({
        title: '提示',
        content: '确认退出？',
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
.mine-page { padding: 24rpx; }
.profile { background: #fff; border-radius: 16rpx; padding: 40rpx; display: flex; align-items: center; margin-bottom: 24rpx; }
.avatar { width: 120rpx; height: 120rpx; border-radius: 50%; background: #007aff; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 48rpx; margin-right: 24rpx; }
.info { display: flex; flex-direction: column; }
.name { font-size: 36rpx; font-weight: bold; }
.role { color: #999; font-size: 26rpx; margin-top: 8rpx; }
.cells { background: #fff; border-radius: 16rpx; margin-bottom: 24rpx; }
.cell { display: flex; justify-content: space-between; padding: 30rpx 24rpx; border-bottom: 1rpx solid #f5f5f5; }
.arrow { color: #999; }
.logout { border-radius: 12rpx; }
</style>
