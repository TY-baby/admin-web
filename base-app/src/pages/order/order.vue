<template>
  <view class='container'>
    <view class='list'>
      <view class='item' v-for='item in list' :key='item.id'>
        <view class='row'><text class='title'>{{ item.order_no }}</text><text class='status'>{{ item.status }}</text></view>
        <view class='row info'><text>客户：{{ item.customer_name }}</text><text>金额：¥{{ item.actual_amount }}</text></view>
      </view>
    </view>
  </view>
</template>

<script>
import { getOrderList } from '@/api/customer.js'
export default {
  data() { return { list: [] } }
  onLoad() { this.load() },
  methods: { async load() { const res = await getOrderList(); this.list = res.list } }
}
</script>

<style>
.container { padding: 20rpx; background: #f5f7fa; min-height: 100vh; }
.list { display: flex; flex-direction: column; gap: 15rpx; }
.item { background: #fff; border-radius: 12rpx; padding: 25rpx; }
.row { display: flex; justify-content: space-between; margin-bottom: 10rpx; }
.title { font-size: 30rpx; font-weight: bold; color: #303133; }
.status { font-size: 24rpx; color: #E6A23C; }
.info { font-size: 26rpx; color: #606266; }
</style>
