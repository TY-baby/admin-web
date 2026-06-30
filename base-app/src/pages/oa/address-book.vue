<template>
  <view class="oa-page">
    <view class="search-bar">
      <input
        v-model="keyword"
        placeholder="搜索姓名 / 部门 / 手机号"
        placeholder-style="color: #c0c4cc"
        class="search-input"
      />
      <text class="search-icon">🔍</text>
    </view>

    <view class="dept-tabs">
      <scroll-view scroll-x class="dept-scroll">
        <view
          class="dept-item"
          v-for="(d, i) in departments"
          :key="i"
          :class="{ active: activeDept === d }"
          @click="activeDept = d"
        >
          {{ d }}
        </view>
      </scroll-view>
    </view>

    <view class="contact-list">
      <view class="contact-card" v-for="(c, i) in filteredContacts" :key="i">
        <view class="contact-avatar" :style="{ background: c.color }">{{ c.name.slice(0, 1) }}</view>
        <view class="contact-info">
          <text class="contact-name">{{ c.name }}</text>
          <text class="contact-dept">{{ c.dept }} · {{ c.position }}</text>
          <text class="contact-phone">{{ c.phone }}</text>
        </view>
        <view class="contact-actions">
          <text class="action-icon" @click="call(c.phone)">📞</text>
          <text class="action-icon" @click="sms(c.phone)">✉️</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      keyword: '',
      activeDept: '全部',
      departments: ['全部', '技术部', '产品部', '销售部', '市场部', '人事部', '财务部'],
      contacts: [
        { name: '张伟', dept: '技术部', position: '前端工程师', phone: '13800138001', color: '#4facfe' },
        { name: '李娜', dept: '产品部', position: '产品经理', phone: '13800138002', color: '#fa709a' },
        { name: '王强', dept: '销售部', position: '销售经理', phone: '13800138003', color: '#43e97b' },
        { name: '刘洋', dept: '市场部', position: '市场专员', phone: '13800138004', color: '#f6d365' },
        { name: '陈静', dept: '人事部', position: 'HRBP', phone: '13800138005', color: '#a18cd1' },
        { name: '赵敏', dept: '财务部', position: '财务主管', phone: '13800138006', color: '#ff9a9e' },
        { name: '孙杰', dept: '技术部', position: '后端工程师', phone: '13800138007', color: '#4facfe' }
      ]
    }
  },
  computed: {
    filteredContacts() {
      return this.contacts.filter(c => {
        const matchDept = this.activeDept === '全部' || c.dept === this.activeDept
        const k = this.keyword.trim()
        const matchKey = !k || c.name.includes(k) || c.dept.includes(k) || c.phone.includes(k)
        return matchDept && matchKey
      })
    }
  },
  methods: {
    call(phone) { uni.makePhoneCall({ phoneNumber: phone }) },
    sms(phone) { uni.showToast({ title: '短信功能待接入', icon: 'none' }) }
  }
}
</script>

<style lang="scss" scoped>
.oa-page { min-height: 100vh; background: #f5f7fa; }

.search-bar {
  position: relative;
  padding: 24rpx 32rpx;
}
.search-input {
  height: 80rpx;
  background: #fff;
  border-radius: 40rpx;
  padding: 0 72rpx 0 32rpx;
  font-size: 28rpx;
  color: #303133;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.04);
}
.search-icon {
  position: absolute;
  right: 56rpx;
  top: 50%;
  transform: translateY(-50%);
  font-size: 32rpx;
}

.dept-tabs {
  background: #fff;
  padding: 16rpx 0;
  border-bottom: 1rpx solid #f2f3f5;
}
.dept-scroll { white-space: nowrap; padding: 0 16rpx; }
.dept-item {
  display: inline-block;
  padding: 12rpx 28rpx;
  margin: 0 8rpx;
  font-size: 26rpx;
  color: #606266;
  background: #f5f7fa;
  border-radius: 28rpx;
  &.active {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: #fff;
  }
}

.contact-list { padding: 24rpx 32rpx 40rpx; }
.contact-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 20rpx;
  padding: 24rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.04);
}
.contact-avatar {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  color: #fff;
  font-size: 34rpx;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
}
.contact-info { flex: 1; }
.contact-name { font-size: 30rpx; color: #303133; font-weight: 600; display: block; }
.contact-dept { font-size: 24rpx; color: #909399; margin-top: 6rpx; display: block; }
.contact-phone { font-size: 24rpx; color: #4facfe; margin-top: 6rpx; display: block; }
.contact-actions { display: flex; gap: 24rpx; }
.action-icon { font-size: 40rpx; }
</style>
