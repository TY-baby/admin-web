<template>
  <view class="oa-page">
    <view class="tab-bar">
      <view
        class="tab-item"
        v-for="(t, i) in tabs"
        :key="i"
        :class="{ active: activeTab === t.key }"
        @click="activeTab = t.key"
      >
        <text>{{ t.label }}</text>
        <text v-if="t.badge" class="tab-badge">{{ t.badge }}</text>
      </view>
    </view>

    <view class="approval-list">
      <view class="approval-card" v-for="(item, i) in filteredList" :key="i">
        <view class="approval-header">
          <view class="approval-type" :style="{ background: item.typeColor }">
            <text>{{ item.type }}</text>
          </view>
          <text class="approval-status" :style="{ color: item.statusColor }">{{ item.status }}</text>
        </view>
        <view class="approval-body">
          <text class="approval-title">{{ item.title }}</text>
          <text class="approval-info">申请人：{{ item.applicant }}</text>
          <text class="approval-info">申请时间：{{ item.time }}</text>
          <text class="approval-amount" v-if="item.amount">金额：¥{{ item.amount }}</text>
        </view>
        <view class="approval-footer" v-if="activeTab === 'pending'">
          <button class="btn reject" @click="handleApprove(item, 'reject')">驳回</button>
          <button class="btn agree" @click="handleApprove(item, 'agree')">同意</button>
        </view>
      </view>

      <view class="empty-tips" v-if="!filteredList.length">
        <text>暂无{{ tabLabel }}事项</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      activeTab: 'pending',
      tabs: [
        { key: 'pending', label: '待审批', badge: 3 },
        { key: 'approved', label: '已审批' },
        { key: 'submitted', label: '我发起的' }
      ],
      list: [
        { type: '请假', typeColor: '#43e97b', title: '张三 申请年假 3 天', applicant: '张三', time: '2026-06-29 10:23', status: '待审批', statusColor: '#f6d365', amount: '', tab: 'pending' },
        { type: '报销', typeColor: '#fa709a', title: '市场部 差旅费报销', applicant: '李四', time: '2026-06-28 16:45', status: '待审批', statusColor: '#f6d365', amount: '1280.00', tab: 'pending' },
        { type: '考勤', typeColor: '#4facfe', title: '王五 外勤打卡异常说明', applicant: '王五', time: '2026-06-28 09:12', status: '待审批', statusColor: '#f6d365', amount: '', tab: 'pending' },
        { type: '请假', typeColor: '#43e97b', title: '赵六 申请事假 1 天', applicant: '赵六', time: '2026-06-25 14:30', status: '已通过', statusColor: '#43e97b', amount: '', tab: 'approved' },
        { type: '报销', typeColor: '#fa709a', title: '本月交通费报销', applicant: '我', time: '2026-06-20 11:00', status: '已通过', statusColor: '#43e97b', amount: '58.00', tab: 'submitted' }
      ]
    }
  },
  computed: {
    tabLabel() {
      const map = { pending: '待审批', approved: '已审批', submitted: '我发起的' }
      return map[this.activeTab]
    },
    filteredList() {
      return this.list.filter(i => i.tab === this.activeTab)
    }
  },
  methods: {
    handleApprove(item, action) {
      const text = action === 'agree' ? '同意' : '驳回'
      uni.showModal({
        title: '确认' + text,
        content: `确定${text}「${item.title}」？`,
        success: res => {
          if (res.confirm) {
            item.status = action === 'agree' ? '已通过' : '已驳回'
            item.statusColor = action === 'agree' ? '#43e97b' : '#fa709a'
            item.tab = 'approved'
            uni.showToast({ title: text + '成功', icon: 'success' })
          }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.oa-page { min-height: 100vh; background: #f5f7fa; }

.tab-bar {
  display: flex;
  background: #fff;
  padding: 0 32rpx;
  border-bottom: 1rpx solid #f2f3f5;
}
.tab-item {
  position: relative;
  flex: 1;
  text-align: center;
  padding: 28rpx 0;
  font-size: 28rpx;
  color: #606266;
  display: flex;
  align-items: center;
  justify-content: center;
  &.active {
    color: #4facfe;
    font-weight: 600;
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 48rpx;
      height: 4rpx;
      background: #4facfe;
      border-radius: 2rpx;
    }
  }
}
.tab-badge {
  background: #fa709a;
  color: #fff;
  font-size: 20rpx;
  padding: 2rpx 10rpx;
  border-radius: 12rpx;
  margin-left: 8rpx;
}

.approval-list { padding: 24rpx 32rpx 40rpx; }
.approval-card {
  background: #fff;
  border-radius: 20rpx;
  padding: 28rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}
.approval-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}
.approval-type {
  font-size: 22rpx;
  color: #fff;
  padding: 4rpx 14rpx;
  border-radius: 8rpx;
}
.approval-status { font-size: 26rpx; font-weight: 600; }
.approval-title { font-size: 30rpx; color: #303133; font-weight: 600; display: block; margin-bottom: 12rpx; }
.approval-info { font-size: 24rpx; color: #909399; display: block; margin-top: 6rpx; }
.approval-amount { font-size: 26rpx; color: #fa709a; margin-top: 10rpx; display: block; font-weight: 600; }

.approval-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 24rpx;
  gap: 16rpx;
}
.btn {
  width: 140rpx;
  height: 64rpx;
  line-height: 64rpx;
  font-size: 26rpx;
  border-radius: 32rpx;
}
.btn::after { border: none; }
.btn.reject { background: #f5f7fa; color: #606266; }
.btn.agree { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: #fff; }

.empty-tips {
  text-align: center;
  padding: 80rpx 0;
  font-size: 26rpx;
  color: #c0c4cc;
}
</style>
