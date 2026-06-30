<template>
  <view class="oa-page">
    <view class="attendance-header">
      <text class="today">{{ today }}</text>
      <text class="status-text">{{ checkedIn ? '已打卡' : '未打卡' }}</text>
      <view class="clock-btn" :class="{ checked: checkedIn }" @click="handleClock">
        <text class="clock-time">{{ currentTime }}</text>
        <text class="clock-label">{{ checkedIn ? '下班打卡' : '上班打卡' }}</text>
      </view>
      <text class="location">📍 {{ location }}</text>
    </view>

    <view class="section-card">
      <text class="section-title">今日统计</text>
      <view class="attendance-stats">
        <view class="a-stat">
          <text class="a-time">{{ record.in || '--:--' }}</text>
          <text class="a-label">上班</text>
        </view>
        <view class="a-line"></view>
        <view class="a-stat">
          <text class="a-time">{{ record.out || '--:--' }}</text>
          <text class="a-label">下班</text>
        </view>
        <view class="a-line"></view>
        <view class="a-stat">
          <text class="a-time">{{ record.hours || '0.0' }}h</text>
          <text class="a-label">工时</text>
        </view>
      </view>
    </view>

    <view class="section-card">
      <text class="section-title">本月记录</text>
      <view class="record-item" v-for="(r, i) in records" :key="i">
        <view class="record-date">
          <text class="rd-day">{{ r.day }}</text>
          <text class="rd-week">{{ r.week }}</text>
        </view>
        <view class="record-info">
          <text class="ri-row">上班 {{ r.in }} · 下班 {{ r.out }}</text>
          <text class="ri-status" :style="{ color: r.statusColor }">{{ r.status }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      checkedIn: false,
      currentTime: '08:30',
      location: '北京市朝阳区科技园 A 座',
      record: { in: '', out: '', hours: '' },
      records: [
        { day: '28', week: '周一', in: '08:55', out: '18:12', status: '正常', statusColor: '#43e97b' },
        { day: '27', week: '周日', in: '--', out: '--', status: '休息', statusColor: '#909399' },
        { day: '26', week: '周六', in: '--', out: '--', status: '休息', statusColor: '#909399' },
        { day: '25', week: '周五', in: '08:48', out: '18:30', status: '正常', statusColor: '#43e97b' },
        { day: '24', week: '周四', in: '09:05', out: '18:20', status: '迟到', statusColor: '#fa709a' }
      ]
    }
  },
  computed: {
    today() {
      const d = new Date()
      return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`
    }
  },
  onLoad() {
    this.tick()
    setInterval(() => this.tick(), 1000)
  },
  methods: {
    tick() {
      const d = new Date()
      this.currentTime = `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
    },
    handleClock() {
      const now = this.currentTime
      if (!this.checkedIn) {
        this.record.in = now
        this.checkedIn = true
        uni.showToast({ title: '上班打卡成功', icon: 'success' })
      } else {
        this.record.out = now
        this.checkedIn = false
        this.record.hours = '8.5'
        uni.showToast({ title: '下班打卡成功', icon: 'success' })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.oa-page { min-height: 100vh; background: #f5f7fa; padding-bottom: 40rpx; }

.attendance-header {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  padding: 40rpx 32rpx 60rpx;
  border-radius: 0 0 40rpx 40rpx;
  text-align: center;
  color: #fff;
}
.today { font-size: 28rpx; opacity: 0.9; display: block; }
.status-text { font-size: 32rpx; font-weight: 600; margin: 16rpx 0 30rpx; display: block; }

.clock-btn {
  width: 280rpx;
  height: 280rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  margin: 0 auto 24rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 20rpx 50rpx rgba(0, 0, 0, 0.15);
  &.checked { background: rgba(255, 255, 255, 0.75); }
}
.clock-time { font-size: 56rpx; font-weight: 700; color: #303133; }
.clock-label { font-size: 28rpx; color: #606266; margin-top: 8rpx; }
.location { font-size: 24rpx; opacity: 0.85; display: block; }

.section-card {
  margin: 24rpx 32rpx;
  background: #fff;
  border-radius: 24rpx;
  padding: 28rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}
.section-title { font-size: 32rpx; font-weight: 700; color: #303133; margin-bottom: 24rpx; display: block; }

.attendance-stats {
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.a-stat { text-align: center; }
.a-time { font-size: 36rpx; font-weight: 700; color: #303133; display: block; }
.a-label { font-size: 24rpx; color: #909399; margin-top: 8rpx; display: block; }
.a-line { width: 2rpx; height: 60rpx; background: #ebeef5; }

.record-item {
  display: flex;
  align-items: center;
  padding: 24rpx 0;
  border-bottom: 1rpx solid #f2f3f5;
  &:last-child { border-bottom: none; }
}
.record-date {
  width: 100rpx;
  text-align: center;
  margin-right: 24rpx;
}
.rd-day { font-size: 40rpx; font-weight: 700; color: #303133; display: block; }
.rd-week { font-size: 22rpx; color: #909399; }
.record-info { flex: 1; }
.ri-row { font-size: 28rpx; color: #606266; display: block; }
.ri-status { font-size: 24rpx; margin-top: 6rpx; display: block; }
</style>
