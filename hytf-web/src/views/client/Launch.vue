<template>
  <div class="client-sub">
    <div class="topbar flex-between">
      <div class="logo" @click="$router.push('/client/home')" style="cursor:pointer">鎭掕€€浜掑ū</div>
      <div><el-button type="text" @click="$router.push('/client/home')">杩斿洖棣栭〉</el-button></div>
    </div>
    <div class="page-container">
      <div class="summary card">
        <div class="flex-between">
          <div><div class="lbl">璐﹀彿鎬讳綑棰?/div><div class="big">锟{ summary.total_balance || 0 }}</div></div>
          <div><div class="lbl">绱鍏呭€?/div><div class="big">锟{ summary.total_recharge || 0 }}</div></div>
          <div><div class="lbl">绱娑堣€?/div><div class="big">锟{ summary.total_consume || 0 }}</div></div>
          <div><div class="lbl">鎶栭煶鍙锋暟</div><div class="big">{{ summary.account_count || 0 }}</div></div>
        </div>
      </div>

      <div class="filter card">
        <span style="margin-right:8px">鏃ユ湡绛涢€?</span>
        <el-date-picker v-model="range" type="daterange" value-format="yyyy-MM-dd"
                        start-placeholder="寮€濮? end-placeholder="缁撴潫" :clearable="false" @change="loadTrend" />
        <el-select v-model="accountId" placeholder="鍏ㄩ儴鎶栭煶鍙? clearable style="margin-left:12px;width:220px" @change="loadTrend">
          <el-option v-for="a in accounts" :key="a.id" :label="a.douyin_name" :value="a.id" />
        </el-select>
        <el-button icon="el-icon-refresh" style="margin-left:8px" @click="loadTrend">鍒锋柊</el-button>
      </div>

      <div class="content">
        <div class="left">
          <div class="modules">
            <div v-for="m in modules" :key="m.key" :class="['mod', activeMod===m.key?'on':'']" @click="selectMod(m.key)">
              <div class="mod-title">{{ m.title }}</div>
              <div class="mod-val">{{ m.value }}</div>
            </div>
          </div>
          <div class="card">
            <line-chart :dates="dates" :series="series" height="360px" />
          </div>
        </div>
        <div class="right card">
          <div class="card-title">鏃ュ父鏂规</div>
          <p>1. 寤鸿姣忔棩鍥哄畾鏃堕棿鏌ョ湅鎶曟斁鏁版嵁锛屼繚鎸佹姇鏀捐妭濂忕ǔ瀹氥€?/p>
          <p>2. 棣栨鎶曟斁鎺ㄨ崘浣跨敤 A 妗ｄ綅锛?00/澶╋級锛岃瀵?3 澶╂晥鏋滃悗鍐嶈皟鏁淬€?/p>
          <p>3. 鑻ュ崟鏃ユ秷鑰楀紓甯告尝鍔ㄨ秴杩?30%锛岃鍙婃椂鑱旂郴瀹㈡湇鏍告煡銆?/p>
          <p>4. 鎺堟潈鍒版湡鍓?3 澶╃郴缁熶細鎻愰啋锛岃鎻愬墠鑱旂郴缁湡閬垮厤涓柇銆?/p>
          <p>5. 鏁版嵁浠ユ湰骞冲彴缁熻涓哄噯锛屽疄闄呮姇鏀炬晥鏋滃彈澶氬洜绱犲奖鍝嶃€?/p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getSummary, getTrend } from '@/api/clientHome'
import LineChart from '@/components/LineChart.vue'

export default {
  name: 'ClientLaunch',
  components: { LineChart },
  data() {
    const today = new Date().toISOString().slice(0, 10)
    return {
      summary: {}, range: [today, today], accountId: '',
      activeMod: 'consume', dates: [], series: [], raw: []
    }
  },
  computed: {
    ...mapState('clientUser', ['accounts']),
    modules() {
      const sum = k => (this.raw || []).reduce((s, x) => s + Number(x[k] || 0), 0).toFixed(2)
      const totalConsume = sum('consume')
      const avg = this.raw.length ? (Number(totalConsume) / this.raw.length).toFixed(2) : '0.00'
      return [
        { key: 'consume', title: '鎬绘秷鑰?, value: '锟? + totalConsume },
        { key: 'recharge', title: '鎬诲厖鍊?, value: '锟? + sum('recharge') },
        { key: 'balance', title: '褰撳墠浣欓', value: '锟? + Number(this.summary.total_balance || 0).toFixed(2) },
        { key: 'avg', title: '鏃ュ潎娑堣€?, value: '锟? + avg }
      ]
    }
  },
  async created() {
    if (!this.accounts.length) await this.$store.dispatch('clientUser/loadAccounts')
    const { data } = await getSummary()
    if (data.code === 0) this.summary = data.data
    this.loadTrend()
  },
  methods: {
    async loadTrend() {
      if (!this.range || this.range.length !== 2) return
      const params = { start: this.range[0], end: this.range[1] }
      if (this.accountId) params.account_id = this.accountId
      const { data } = await getTrend(params)
      if (data.code === 0) {
        this.raw = data.data.items || []
        this.dates = this.raw.map(x => x.date)
        this.applySeries()
      }
    },
    selectMod(k) { this.activeMod = k; this.applySeries() },
    applySeries() {
      const key = this.activeMod
      const nameMap = { consume: '娑堣€?, recharge: '鍏呭€?, balance: '浣欓', avg: '鏃ュ潎娑堣€? }
      const colorMap = { consume: '#F56C6C', recharge: '#67C23A', balance: '#409EFF', avg: '#E6A23C' }
      if (key === 'avg') {
        const total = (this.raw || []).reduce((s, x) => s + Number(x.consume || 0), 0)
        const avg = this.raw.length ? total / this.raw.length : 0
        this.series = [{ name: nameMap[key], data: this.raw.map(() => Number(avg.toFixed(2))), color: colorMap[key] }]
      } else {
        this.series = [{ name: nameMap[key], data: this.raw.map(x => Number(x[key] || 0)), color: colorMap[key] }]
      }
    }
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
  background: #fff; border-radius: 6px; padding: 16px; margin-bottom: 16px;
  .card-title { font-size: 15px; font-weight: bold; margin-bottom: 12px; }
}
.summary {
  .lbl { color: #909399; font-size: 13px; }
  .big { font-size: 22px; font-weight: bold; color: #303133; margin-top: 4px; }
}
.content {
  display: flex; gap: 16px;
  .left { flex: 2; }
  .right { flex: 1; line-height: 1.9; color: #606266; font-size: 13px; }
}
.modules {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px;
  .mod {
    background: #fff; padding: 16px; border-radius: 6px; cursor: pointer;
    border: 2px solid transparent;
    &.on { border-color: #409EFF; }
    .mod-title { color: #909399; font-size: 13px; }
    .mod-val { font-size: 20px; font-weight: bold; color: #303133; margin-top: 6px; }
  }
}
</style>