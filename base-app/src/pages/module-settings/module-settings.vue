<template>
  <view class="oa-page">
    <view class="tips-card">
      <text class="tips-text">💡 点击模块可添加或移除首页应用入口，长按可拖动排序（当前版本支持点击切换）</text>
    </view>

    <view class="section-card">
      <text class="section-title">已显示应用</text>
      <view class="module-list">
        <view
          class="module-item active"
          v-for="(m, i) in visibleModules"
          :key="m.key"
          @click="toggle(m.key)"
        >
          <view class="module-icon" :style="{ background: m.color }">{{ m.icon }}</view>
          <text class="module-label">{{ m.label }}</text>
          <view class="module-check">✓</view>
        </view>
      </view>
    </view>

    <view class="section-card">
      <text class="section-title">未显示应用</text>
      <view class="module-list">
        <view
          class="module-item"
          v-for="(m, i) in hiddenModules"
          :key="m.key"
          @click="toggle(m.key)"
        >
          <view class="module-icon" :style="{ background: m.color }">{{ m.icon }}</view>
          <text class="module-label">{{ m.label }}</text>
          <view class="module-add">+</view>
        </view>
      </view>
    </view>

    <button class="reset-btn" @click="reset">恢复默认</button>
  </view>
</template>

<script>
export default {
  computed: {
    modules() {
      return this.$store.getters['app/moduleList']
    },
    visibleModules() {
      return this.modules.filter(m => m.visible)
    },
    hiddenModules() {
      return this.modules.filter(m => !m.visible)
    }
  },
  methods: {
    toggle(key) {
      this.$store.commit('app/TOGGLE_MODULE', key)
    },
    reset() {
      uni.showModal({
        title: '提示',
        content: '确定恢复默认模块布局？',
        success: res => {
          if (res.confirm) this.$store.commit('app/RESET')
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.oa-page { min-height: 100vh; background: #f5f7fa; padding: 24rpx 32rpx 40rpx; }

.tips-card {
  background: #e0f7fa;
  border-radius: 16rpx;
  padding: 20rpx 24rpx;
  margin-bottom: 24rpx;
}
.tips-text { font-size: 24rpx; color: #00838f; line-height: 1.5; }

.section-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 28rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}
.section-title { font-size: 32rpx; font-weight: 700; color: #303133; margin-bottom: 24rpx; display: block; }

.module-list {
  display: flex;
  flex-wrap: wrap;
}
.module-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 28rpx;
  position: relative;
}
.module-icon {
  width: 92rpx;
  height: 92rpx;
  border-radius: 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 44rpx;
  margin-bottom: 12rpx;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.08);
}
.module-label { font-size: 24rpx; color: #606266; }
.module-check, .module-add {
  position: absolute;
  top: -6rpx;
  right: 10rpx;
  width: 32rpx;
  height: 32rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
  color: #fff;
}
.module-check { background: #43e97b; }
.module-add { background: #c0c4cc; }

.reset-btn {
  height: 92rpx;
  line-height: 92rpx;
  border-radius: 46rpx;
  background: #fff;
  color: #606266;
  font-size: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.04);
}
.reset-btn::after { border: none; }
</style>
