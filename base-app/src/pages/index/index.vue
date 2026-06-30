<template>
  <view class="workplace">
    <!-- 顶部背景 + 用户信息 -->
    <view class="header-card">
      <view class="header-top">
        <view class="greeting">
          <text class="hello">{{ greeting }}，{{ userName }}</text>
          <text class="date">{{ today }} · {{ weekDay }}</text>
        </view>
        <view class="avatar" @click="goMine">{{ avatarText }}</view>
      </view>

      <view class="quick-stats">
        <view class="stat-item" v-for="(s, i) in statsList" :key="i">
          <text class="stat-num">{{ s.value }}</text>
          <text class="stat-name">{{ s.label }}</text>
        </view>
      </view>
    </view>

    <!-- 公告滚动 -->
    <view class="notice-bar" @click="goNotice">
      <text class="notice-tag">公告</text>
      <swiper class="notice-swiper" vertical autoplay circular interval="3000">
        <swiper-item v-for="(n, i) in notices" :key="i">
          <text class="notice-text">{{ n.title }}</text>
        </swiper-item>
      </swiper>
      <text class="notice-arrow">›</text>
    </view>

    <!-- 应用入口 -->
    <view class="section-card">
      <view class="section-header">
        <text class="section-title">应用中心</text>
        <view class="edit-btn" @click="goModuleSettings">
          <text>自定义</text>
          <text class="arrow">›</text>
        </view>
      </view>
      <view class="app-grid">
        <view
          class="app-item"
          v-for="(m, i) in homeModules"
          :key="i"
          @click="navigate(m.path)"
        >
          <view class="app-icon" :style="{ background: m.color }">
            <text>{{ m.icon }}</text>
          </view>
          <text class="app-label">{{ m.label }}</text>
        </view>
        <view class="app-item" @click="goModuleSettings">
          <view class="app-icon more">
            <text>⚙️</text>
          </view>
          <text class="app-label">更多</text>
        </view>
      </view>
    </view>

    <!-- 待办 / 审批 -->
    <view class="section-card">
      <view class="section-header">
        <text class="section-title">待办事项</text>
        <text class="view-all" @click="goApproval">查看全部</text>
      </view>
      <view class="todo-list">
        <view
          class="todo-item"
          v-for="(t, i) in todos"
          :key="i"
          @click="goApproval"
        >
          <view class="todo-dot" :style="{ background: t.color }"></view>
          <view class="todo-main">
            <text class="todo-title">{{ t.title }}</text>
            <text class="todo-time">{{ t.time }}</text>
          </view>
          <text class="todo-status" :style="{ color: t.color }">{{ t.status }}</text>
        </view>
        <view class="empty-tips" v-if="!todos.length">
          <text>暂无待办事项，工作顺心 🎉</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getStats } from '@/api/customer.js'

export default {
  data() {
    return {
      stats: {},
      notices: [
        { title: '关于 2026 年端午节放假安排的通知' },
        { title: '新员工入职培训定于本周五下午 2 点' },
        { title: '公司新版 CRM 移动端正式上线啦' }
      ],
      todos: [
        { title: '张三 提交的请假申请待审批', time: '10:23', status: '待审批', color: '#fa709a' },
        { title: '市场部 费用报销单待审核', time: '昨天', status: '待处理', color: '#f6d365' },
        { title: '李四 外勤打卡异常说明', time: '昨天', status: '待查看', color: '#4facfe' }
      ]
    }
  },
  computed: {
    userName() {
      const info = this.$store.state.user.userInfo
      return info.real_name || info.username || '同事'
    },
    avatarText() {
      const name = this.userName
      return name.slice(0, 1).toUpperCase()
    },
    greeting() {
      const h = new Date().getHours()
      if (h < 12) return '早上好'
      if (h < 14) return '中午好'
      if (h < 19) return '下午好'
      return '晚上好'
    },
    today() {
      const d = new Date()
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
    },
    weekDay() {
      const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
      return days[new Date().getDay()]
    },
    statsList() {
      return [
        { label: '客户', value: this.stats.totalCustomers || 0 },
        { label: '商机', value: this.stats.totalOpportunities || 0 },
        { label: '订单', value: this.stats.totalOrders || 0 },
        { label: '金额', value: '¥' + (this.stats.totalAmount || 0) }
      ]
    },
    homeModules() {
      return this.$store.getters['app/homeModules']
    }
  },
  onShow() {
    this.loadStats()
  },
  methods: {
    async loadStats() {
      try {
        this.stats = await getStats()
      } catch (e) {
        console.warn('获取统计数据失败', e)
      }
    },
    navigate(url) {
      // tabBar 页面用 switchTab，普通页面用 navigateTo
      const tabPages = ['/pages/index/index', '/pages/customer/customer', '/pages/mine/mine']
      if (tabPages.includes(url)) {
        uni.switchTab({ url })
      } else {
        uni.navigateTo({ url })
      }
    },
    goMine() { uni.switchTab({ url: '/pages/mine/mine' }) },
    goNotice() { uni.navigateTo({ url: '/pages/oa/notice' }) },
    goApproval() { uni.navigateTo({ url: '/pages/oa/approval' }) },
    goModuleSettings() { uni.navigateTo({ url: '/pages/module-settings/module-settings' }) }
  }
}
</script>

<style lang="scss" scoped>
.workplace {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 40rpx;
}

.header-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  padding: 60rpx 32rpx 50rpx;
  border-radius: 0 0 40rpx 40rpx;
  color: #fff;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40rpx;
}

.hello {
  font-size: 40rpx;
  font-weight: 700;
  display: block;
}
.date {
  font-size: 24rpx;
  opacity: 0.85;
  margin-top: 8rpx;
  display: block;
}
.avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  font-weight: 700;
  backdrop-filter: blur(10rpx);
}

.quick-stats {
  display: flex;
  justify-content: space-around;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20rpx;
  padding: 24rpx 0;
  backdrop-filter: blur(10rpx);
}
.stat-item { text-align: center; }
.stat-num { font-size: 36rpx; font-weight: 700; display: block; }
.stat-name { font-size: 22rpx; opacity: 0.9; margin-top: 6rpx; display: block; }

.notice-bar {
  margin: 24rpx 32rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 20rpx 24rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}
.notice-tag {
  background: #ffecd2;
  color: #f6a93b;
  font-size: 22rpx;
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
  margin-right: 16rpx;
  font-weight: 600;
}
.notice-swiper {
  flex: 1;
  height: 40rpx;
}
.notice-text {
  font-size: 26rpx;
  color: #606266;
  line-height: 40rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.notice-arrow {
  color: #c0c4cc;
  font-size: 32rpx;
  margin-left: 12rpx;
}

.section-card {
  margin: 24rpx 32rpx;
  background: #fff;
  border-radius: 24rpx;
  padding: 28rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}
.section-title { font-size: 32rpx; font-weight: 700; color: #303133; }
.edit-btn, .view-all {
  display: flex;
  align-items: center;
  font-size: 24rpx;
  color: #909399;
}
.edit-btn .arrow { margin-left: 4rpx; }

.app-grid {
  display: flex;
  flex-wrap: wrap;
}
.app-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 24rpx;
}
.app-icon {
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
.app-icon.more { background: #f2f3f5; }
.app-label { font-size: 24rpx; color: #606266; }

.todo-list {
  .todo-item {
    display: flex;
    align-items: center;
    padding: 24rpx 0;
    border-bottom: 1rpx solid #f2f3f5;
    &:last-child { border-bottom: none; }
  }
}
.todo-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  margin-right: 20rpx;
  flex-shrink: 0;
}
.todo-main { flex: 1; }
.todo-title { font-size: 28rpx; color: #303133; display: block; }
.todo-time { font-size: 22rpx; color: #c0c4cc; margin-top: 6rpx; display: block; }
.todo-status { font-size: 24rpx; flex-shrink: 0; }
.empty-tips {
  text-align: center;
  padding: 40rpx 0;
  font-size: 26rpx;
  color: #c0c4cc;
}
</style>
