<template>
  <div class="client-sub">
    <div class="topbar flex-between">
      <div class="logo">鎭掕€€浜掑ū - 璐㈠姟</div>
      <div><el-button type="text" @click="$router.push('/client/home')">杩斿洖棣栭〉</el-button></div>
    </div>
    <div class="page-container">
      <div class="card">
        <div class="card-title">鎴戠殑璧勯噾</div>
        <el-table :data="rows" border stripe>
          <el-table-column prop="douyin_name" label="鎶栭煶鍙? />
          <el-table-column prop="douyin_id" label="鎶栭煶ID" />
          <el-table-column prop="recharge_amount" label="鍏呭€奸噾棰?鍏?" width="130" />
          <el-table-column prop="balance" label="鍓╀綑娴佹按(鍏?" width="130" />
          <el-table-column prop="tier" label="妗ｄ綅" width="80" />
          <el-table-column prop="tier_daily_budget" label="鏃ラ绠? width="100" />
        </el-table>
        <div class="text-muted mt-16">浜ゆ槗鍧囦负绾夸笅澶勭悊锛屾澶勪粎浣滅櫥璁板睍绀猴紝濡傞渶鍏呭€艰鑱旂郴瀹㈡湇銆?/div>
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