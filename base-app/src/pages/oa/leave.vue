<template>
  <view class="oa-page">
    <view class="form-card">
      <text class="form-title">请假申请</text>

      <view class="form-item">
        <text class="label">请假类型</text>
        <picker mode="selector" :range="leaveTypes" :value="typeIndex" @change="onTypeChange">
          <view class="picker-value">{{ leaveTypes[typeIndex] }}</view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label">开始时间</text>
        <picker mode="date" :value="form.startDate" @change="e => form.startDate = e.detail.value">
          <view class="picker-value">{{ form.startDate || '请选择' }}</view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label">结束时间</text>
        <picker mode="date" :value="form.endDate" @change="e => form.endDate = e.detail.value">
          <view class="picker-value">{{ form.endDate || '请选择' }}</view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label">请假事由</text>
        <textarea
          v-model="form.reason"
          placeholder="请填写请假原因..."
          placeholder-style="color: #c0c4cc"
          class="textarea"
        />
      </view>

      <button class="submit-btn" @click="submit">提交申请</button>
    </view>

    <view class="form-card">
      <text class="form-title">我的请假记录</text>
      <view class="record-row" v-for="(r, i) in records" :key="i">
        <view class="record-main">
          <text class="r-type">{{ r.type }}</text>
          <text class="r-date">{{ r.start }} 至 {{ r.end }}</text>
        </view>
        <text class="r-status" :style="{ color: r.color }">{{ r.status }}</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      leaveTypes: ['事假', '病假', '年假', '调休', '婚假', '产假'],
      typeIndex: 0,
      form: {
        startDate: '',
        endDate: '',
        reason: ''
      },
      records: [
        { type: '年假', start: '2026-06-25', end: '2026-06-27', status: '已通过', color: '#43e97b' },
        { type: '事假', start: '2026-05-10', end: '2026-05-10', status: '已通过', color: '#43e97b' },
        { type: '病假', start: '2026-04-02', end: '2026-04-03', status: '已驳回', color: '#fa709a' }
      ]
    }
  },
  methods: {
    onTypeChange(e) {
      this.typeIndex = e.detail.value
    },
    submit() {
      if (!this.form.startDate || !this.form.endDate || !this.form.reason) {
        return uni.showToast({ title: '请填写完整信息', icon: 'none' })
      }
      uni.showToast({ title: '提交成功', icon: 'success' })
      this.records.unshift({
        type: this.leaveTypes[this.typeIndex],
        start: this.form.startDate,
        end: this.form.endDate,
        status: '审批中',
        color: '#f6d365'
      })
      this.form = { startDate: '', endDate: '', reason: '' }
    }
  }
}
</script>

<style lang="scss" scoped>
.oa-page { min-height: 100vh; background: #f5f7fa; padding: 24rpx 32rpx 40rpx; }

.form-card {
  background: #fff;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}
.form-title { font-size: 32rpx; font-weight: 700; color: #303133; margin-bottom: 28rpx; display: block; }

.form-item { margin-bottom: 28rpx; }
.label { font-size: 26rpx; color: #606266; margin-bottom: 12rpx; display: block; }
.picker-value {
  height: 84rpx;
  line-height: 84rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
  padding: 0 24rpx;
  font-size: 28rpx;
  color: #303133;
}
.textarea {
  width: 100%;
  height: 180rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
  padding: 20rpx 24rpx;
  font-size: 28rpx;
  color: #303133;
  box-sizing: border-box;
}

.submit-btn {
  height: 92rpx;
  line-height: 92rpx;
  border-radius: 46rpx;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: #fff;
  font-size: 32rpx;
  font-weight: 600;
  box-shadow: 0 12rpx 32rpx rgba(67, 233, 123, 0.3);
}
.submit-btn::after { border: none; }

.record-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24rpx 0;
  border-bottom: 1rpx solid #f2f3f5;
  &:last-child { border-bottom: none; }
}
.record-main { flex: 1; }
.r-type { font-size: 30rpx; color: #303133; font-weight: 600; display: block; }
.r-date { font-size: 24rpx; color: #909399; margin-top: 6rpx; display: block; }
.r-status { font-size: 26rpx; }
</style>
