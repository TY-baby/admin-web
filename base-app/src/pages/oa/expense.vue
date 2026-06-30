<template>
  <view class="oa-page">
    <view class="form-card">
      <text class="form-title">费用报销</text>

      <view class="form-item">
        <text class="label">报销类型</text>
        <picker mode="selector" :range="expenseTypes" :value="typeIndex" @change="onTypeChange">
          <view class="picker-value">{{ expenseTypes[typeIndex] }}</view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label">报销金额（元）</text>
        <input
          v-model="form.amount"
          type="digit"
          placeholder="0.00"
          placeholder-style="color: #c0c4cc"
          class="input"
        />
      </view>

      <view class="form-item">
        <text class="label">发生日期</text>
        <picker mode="date" :value="form.date" @change="e => form.date = e.detail.value">
          <view class="picker-value">{{ form.date || '请选择' }}</view>
        </picker>
      </view>

      <view class="form-item">
        <text class="label">费用说明</text>
        <textarea
          v-model="form.desc"
          placeholder="请填写费用明细..."
          placeholder-style="color: #c0c4cc"
          class="textarea"
        />
      </view>

      <view class="form-item">
        <text class="label">上传发票</text>
        <view class="upload-box" @click="chooseImage">
          <text class="upload-icon">📷</text>
          <text class="upload-text">点击上传发票照片</text>
        </view>
      </view>

      <button class="submit-btn" @click="submit">提交报销</button>
    </view>

    <view class="form-card">
      <text class="form-title">报销记录</text>
      <view class="record-row" v-for="(r, i) in records" :key="i">
        <view class="record-main">
          <text class="r-type">{{ r.type }} · ¥{{ r.amount }}</text>
          <text class="r-date">{{ r.date }}</text>
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
      expenseTypes: ['差旅费', '交通费', '餐饮费', '办公用品', '招待费', '其他'],
      typeIndex: 0,
      form: { amount: '', date: '', desc: '' },
      records: [
        { type: '差旅费', amount: '1280.00', date: '2026-06-20', status: '已通过', color: '#43e97b' },
        { type: '餐饮费', amount: '286.50', date: '2026-06-15', status: '审批中', color: '#f6d365' },
        { type: '交通费', amount: '58.00', date: '2026-06-08', status: '已驳回', color: '#fa709a' }
      ]
    }
  },
  methods: {
    onTypeChange(e) {
      this.typeIndex = e.detail.value
    },
    chooseImage() {
      uni.chooseImage({
        count: 1,
        success: () => uni.showToast({ title: '已选择图片', icon: 'success' })
      })
    },
    submit() {
      if (!this.form.amount || !this.form.date || !this.form.desc) {
        return uni.showToast({ title: '请填写完整信息', icon: 'none' })
      }
      uni.showToast({ title: '提交成功', icon: 'success' })
      this.records.unshift({
        type: this.expenseTypes[this.typeIndex],
        amount: this.form.amount,
        date: this.form.date,
        status: '审批中',
        color: '#f6d365'
      })
      this.form = { amount: '', date: '', desc: '' }
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
.input, .picker-value {
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
  height: 160rpx;
  background: #f5f7fa;
  border-radius: 12rpx;
  padding: 20rpx 24rpx;
  font-size: 28rpx;
  color: #303133;
  box-sizing: border-box;
}

.upload-box {
  height: 180rpx;
  background: #f5f7fa;
  border: 2rpx dashed #dcdfe6;
  border-radius: 12rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.upload-icon { font-size: 48rpx; }
.upload-text { font-size: 24rpx; color: #909399; margin-top: 8rpx; }

.submit-btn {
  height: 92rpx;
  line-height: 92rpx;
  border-radius: 46rpx;
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: #fff;
  font-size: 32rpx;
  font-weight: 600;
  box-shadow: 0 12rpx 32rpx rgba(250, 112, 154, 0.3);
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
