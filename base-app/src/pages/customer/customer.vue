<template>
  <view class='container'>
    <view class='search-bar'>
      <input class='search-input' v-model='keyword' placeholder='搜索客户名称/电话' />
      <button class='search-btn' @click='load'>搜索</button>
    </view>
    <view class='customer-list'>
      <view class='customer-item' v-for='item in list' :key='item.id'>
        <view class='customer-top'>
          <text class='name'>{{ item.name }}</text>
          <text class='status'>{{ item.status }}</text>
        </view>
        <view class='customer-info'>
          <text>{{ item.company }}</text>
          <text>{{ item.phone }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getCustomerList } from '@/api/customer.js'
export default {
  data() { return { keyword: '', list: [], page: 1, size: 10, total: 0 } }
  onLoad() { this.load() },
  onReachBottom() { if (this.list.length < this.total) { this.page++; this.load() } }
  methods: {
    async load() {
      const res = await getCustomerList({ keyword: this.keyword, page: this.page, size: this.size })
      this.list = this.page === 1 ? res.list : [...this.list, ...res.list]
      this.total = res.total
    }
  }
}
</script>

<style>
.container { padding: 20rpx; background: #f5f7fa; min-height: 100vh; }
.search-bar { display: flex; gap: 15rpx; margin-bottom: 20rpx; }
.search-input { flex: 1; background: #fff; border-radius: 8rpx; padding: 15rpx 20rpx; font-size: 28rpx; }
.search-btn { background: #409EFF; color: #fff; border: none; border-radius: 8rpx; padding: 0 30rpx; font-size: 28rpx; }
.customer-list { display: flex; flex-direction: column; gap: 15rpx; }
.customer-item { background: #fff; border-radius: 12rpx; padding: 25rpx; box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05); }
.customer-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15rpx; }
.name { font-size: 32rpx; font-weight: bold; color: #303133; }
.status { font-size: 24rpx; color: #409EFF; background: rgba(64,158,255,0.1); padding: 4rpx 12rpx; border-radius: 6rpx; }
.customer-info { display: flex; flex-direction: column; gap: 8rpx; font-size: 26rpx; color: #606266; }
</style>
