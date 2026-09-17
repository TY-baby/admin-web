<template>
  <div class="client-sub">
    <div class="topbar flex-between">
      <div class="logo">恒耀互娱 - 财务</div>
      <div><el-button type="text" @click="$router.push('/client/home')">返回首页</el-button></div>
    </div>
    <div class="page-container">
      <div class="card">
        <div class="card-title">我的资金</div>
        <el-table :data="rows" border stripe>
          <el-table-column prop="douyin_name" label="抖音号" />
          <el-table-column prop="douyin_id" label="抖音ID" />
          <el-table-column prop="recharge_amount" label="充值金额(元)" width="130" />
          <el-table-column prop="balance" label="剩余流水(元)" width="130" />
          <el-table-column prop="tier" label="档位" width="80" />
          <el-table-column prop="tier_daily_budget" label="日预算" width="100" />
        </el-table>
        <div class="text-muted mt-16">交易均为线下处理，此处仅作登记展示，如需充值请联系客服。</div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'ClientFinance',
  computed: { ...mapState('clientUser', ['accounts']), rows() { return this.accounts || [] } },
  async created() {
    if (!this.accounts.length) await this.$store.dispatch('clientUser/loadAccounts')
  }
}
</script>

<style scoped lang="scss">
.client-sub { min-height: 100vh; background: #f5f7fa; }
.topbar {
  height: 56px; background: #fff; padding: 0 24px; border-bottom: 1px solid #eee;
  .logo { font-weight: bold; font-size: 18px; color: #1e3c72; }
}
.card {
  background: #fff; padding: 16px; border-radius: 6px;
  .card-title { font-size: 15px; font-weight: bold; margin-bottom: 12px; }
}
</style>