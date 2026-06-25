<template>
  <view class='container'>
    <view class='header'>
      <text class='title'>Base Room 移动CRM</text>
      <text class='subtitle'>{{ today }}</text>
    </view>
    <view class='stats-grid'>
      <view class='stat-card' v-for='(s, i) in statsList' :key='i'>
        <text class='stat-value'>{{ s.value }}</text>
        <text class='stat-label'>{{ s.label }}</text>
      </view>
    </view>
    <view class='menu-grid'>
      <view class='menu-item' v-for='(m, i) in menus' :key='i' @click='navigate(m.url)'>
        <text class='menu-icon'>{{ m.icon }}</text>
        <text class='menu-label'>{{ m.label }}</text>
      </view>
    </view>
  </view>
</template>

<script>
import { getStats } from '@/api/customer.js'
export default {
  data() {
    return {
      today: '',
      stats: {}
    }
  },
  computed: {
    statsList() {
      return [
        { label: '客户', value: this.stats.totalCustomers || 0 },
        { label: '商机', value: this.stats.totalOpportunities || 0 },
        { label: '订单', value: this.stats.totalOrders || 0 },
        { label: '金额', value: '¥' + (this.stats.totalAmount || 0) }
      ]
    },
    menus() {
      return [
        { label: '客户管理', icon: '👤', url: '/pages/customer/customer' },
        { label: '商机管理', icon: '📈', url: '/pages/opportunity/opportunity' },
        { label: '订单管理', icon: '📋', url: '/pages/order/order' },
        { label: '跟进记录', icon: '📞', url: '/pages/follow/follow' },
        { label: '智慧大屏', icon: '🖥️', url: '/pages/bigscreen/bigscreen' },
        { label: '个人中心', icon: '👤', url: '/pages/mine/mine' }
      ]
    }
  },
  onLoad() {
    const d = new Date()
    this.today = d.getFullYear() + '年' + (d.getMonth()+1) + '月' + d.getDate() + '日'
    this.loadStats()
  },
  methods: {
    async loadStats() {
      try { this.stats = await getStats() } catch(e) {}
    },
    navigate(url) { uni.navigateTo({ url }) }
  }
}
</script>

<style>
.container { padding: 20rpx; background: #f5f7fa; min-height: 100vh; }
.header { padding: 30rpx; background: linear-gradient(135deg, #409EFF, #36D1DC); border-radius: 16rpx; color: #fff; margin-bottom: 20rpx; }
.title { font-size: 40rpx; font-weight: bold; display: block; }
.subtitle { font-size: 24rpx; opacity: 0.9; margin-top: 10rpx; display: block; }
.stats-grid { display: flex; flex-wrap: wrap; gap: 20rpx; margin-bottom: 20rpx; }
.stat-card { width: calc(25% - 15rpx); background: #fff; border-radius: 12rpx; padding: 20rpx; text-align: center; box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05); }
.stat-value { font-size: 32rpx; font-weight: bold; color: #303133; display: block; }
.stat-label { font-size: 22rpx; color: #909399; margin-top: 8rpx; display: block; }
.menu-grid { display: flex; flex-wrap: wrap; gap: 20rpx; }
.menu-item { width: calc(33.33% - 14rpx); background: #fff; border-radius: 12rpx; padding: 30rpx; text-align: center; box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05); }
.menu-icon { font-size: 48rpx; display: block; margin-bottom: 10rpx; }
.menu-label { font-size: 26rpx; color: #606266; }
</style>
