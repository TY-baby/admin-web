<template>
  <view class='container'>
    <view class='input-bar'>
      <input v-model='form.customer_id' placeholder='客户ID' class='input' />
      <textarea v-model='form.content' placeholder='跟进内容' class='textarea' />
      <button class='btn' @click='submit'>提交跟进</button>
    </view>
  </view>
</template>

<script>
import request from '@/utils/request.js'
export default {
  data() { return { form: { customer_id: '', content: '', follow_type: '电话' } } }
  methods: {
    async submit() {
      await request.post('/follows', this.form)
      uni.showToast({ title: '提交成功', icon: 'success' })
      this.form = { customer_id: '', content: '', follow_type: '电话' }
    }
  }
}
</script>

<style>
.container { padding: 20rpx; background: #f5f7fa; min-height: 100vh; }
.input-bar { display: flex; flex-direction: column; gap: 20rpx; }
.input, .textarea { background: #fff; border-radius: 12rpx; padding: 20rpx; font-size: 28rpx; }
.textarea { height: 200rpx; }
.btn { background: #409EFF; color: #fff; border: none; border-radius: 12rpx; font-size: 30rpx; }
</style>
