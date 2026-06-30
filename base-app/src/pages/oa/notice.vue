<template>
  <view class="oa-page">
    <view class="notice-card" v-for="(n, i) in notices" :key="i" @click="viewDetail(n)">
      <view class="notice-top">
        <text class="notice-tag" :style="{ background: n.tagColor, color: n.tagTextColor }">{{ n.tag }}</text>
        <text class="notice-date">{{ n.date }}</text>
      </view>
      <text class="notice-title">{{ n.title }}</text>
      <text class="notice-summary">{{ n.summary }}</text>
      <view class="notice-bottom">
        <text class="notice-author">{{ n.author }}</text>
        <text class="notice-read">{{ n.readCount }} 阅读</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      notices: [
        { tag: '重要', tagColor: '#ffecd2', tagTextColor: '#f6a93b', title: '关于 2026 年端午节放假安排的通知', summary: '2026 年端午节放假时间为 6 月 22 日至 6 月 24 日，共 3 天。请各部门提前做好工作安排。', date: '2026-06-15', author: '行政部', readCount: 128 },
        { tag: '公告', tagColor: '#e0f7fa', tagTextColor: '#00acc1', title: '公司新版 CRM 移动端正式上线', summary: '新版移动端已开放使用，支持客户管理、审批、考勤等功能，请大家及时体验。', date: '2026-06-28', author: '产品部', readCount: 86 },
        { tag: '培训', tagColor: '#e8f5e9', tagTextColor: '#43a047', title: '新员工入职培训通知', summary: '本周五下午 2 点将在 3 楼会议室举行新员工入职培训，请相关人员准时参加。', date: '2026-06-29', author: '人力资源部', readCount: 45 },
        { tag: '活动', tagColor: '#f3e5f5', tagTextColor: '#8e24aa', title: '7 月团建活动报名', summary: '拟定于 7 月中旬组织户外团建，请大家积极报名，具体行程后续通知。', date: '2026-06-30', author: '企业文化部', readCount: 210 }
      ]
    }
  },
  methods: {
    viewDetail(n) {
      uni.showModal({
        title: n.title,
        content: n.summary,
        showCancel: false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.oa-page { min-height: 100vh; background: #f5f7fa; padding: 24rpx 32rpx 40rpx; }

.notice-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}
.notice-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}
.notice-tag {
  font-size: 22rpx;
  padding: 4rpx 14rpx;
  border-radius: 8rpx;
  font-weight: 600;
}
.notice-date { font-size: 24rpx; color: #c0c4cc; }
.notice-title { font-size: 30rpx; color: #303133; font-weight: 600; display: block; margin-bottom: 12rpx; }
.notice-summary {
  font-size: 26rpx;
  color: #606266;
  line-height: 1.6;
  display: block;
  margin-bottom: 16rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
.notice-bottom {
  display: flex;
  justify-content: space-between;
  font-size: 24rpx;
  color: #909399;
}
</style>
