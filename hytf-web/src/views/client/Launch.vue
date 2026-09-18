<template>
  <div class="client-sub">
    <div class="topbar flex-between">
      <div class="logo" @click="$router.push('/client/home')" style="cursor:pointer">恒耀互娱</div>
      <div><el-button type="text" @click="$router.push('/client/home')">返回首页</el-button></div>
    </div>
    <div class="page-container">
      <div class="summary card">
        <div class="flex-between">
          <div><div class="lbl">账号总余额</div><div class="big">￥{{ summary.total_balance || 0 }}</div></div>
          <div><div class="lbl">累计充值</div><div class="big">￥{{ summary.total_recharge || 0 }}</div></div>
          <div><div class="lbl">累计消费</div><div class="big">￥{{ summary.total_consume || 0 }}</div></div>
          <div><div class="lbl">抖音号数</div><div class="big">{{ summary.account_count || 0 }}</div></div>
        </div>
      </div>

      <div class="filter card">
        <span style="margin-right:8px">日期筛选</span>
        <el-date-picker v-model="range" type="daterange" value-format="yyyy-MM-dd"
                        start-placeholder="开始" end-placeholder="结束" :clearable="false" @change="loadTrend" />
        <el-select v-model="accountId" placeholder="全部抖音号" clearable style="margin-left:12px;width:220px" @change="loadTrend">
          <el-option v-for="a in accounts" :key="a.id" :label="a.douyin_name" :value="a.id" />
        </el-select>
        <el-button icon="el-icon-refresh" style="margin-left:8px" @click="loadTrend">刷新</el-button>
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
          <div class="card-title">日常方案</div>
          <p>1. 建议每日固定时间查看投放数据，保持投放节奏稳定。</p>
          <p>2. 首次投放推荐使用 A 档位（300/天），观察 3 天效果后再调整。</p>
          <p>3. 若单日消耗异常波动超过 30%，请及时联系客服核查。</p>
          <p>4. 授权到期前 3 天系统会提醒，请提前联系续期避免中断。</p>
          <p>5. 数据以本平台统计为准，实际投放效果受多因素影响。</p>
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
        { key: 'consume', title: '总消费', value: '￥' + totalConsume },
        { key: 'recharge', title: '总充值', value: '￥' + sum('recharge') },
        { key: 'balance', title: '当前余额', value: '￥' + Number(this.summary.total_balance || 0).toFixed(2) },
        { key: 'avg', title: '日均消费', value: '￥' + avg }
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
      const nameMap = { consume: '消费', recharge: '充值', balance: '余额', avg: '日均消费' }
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
.client-sub { min-height: 100vh; background: linear-gradient(160deg, #fff0f5 0%, #ffe8ef 45%, #ffeef4 100%); }
.topbar {
  height: 56px; padding: 0 24px;
  background: linear-gradient(135deg, #ff5f8f 0%, #ff2e63 100%);
  box-shadow: 0 2px 12px rgba(255, 46, 99, .25);
  .logo { font-weight: bold; font-size: 18px; color: #fff; }
  ::v-deep .el-button--text { color: #fff; }
}
.card {
  background: #fff; border-radius: 12px; padding: 18px; margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(255, 46, 99, .08);
  .card-title { font-size: 15px; font-weight: bold; margin-bottom: 12px;
    border-left: 3px solid #ff2e63; padding-left: 8px; }
}
.summary {
  .lbl { color: #909399; font-size: 13px; }
  .big { font-size: 22px; font-weight: bold; color: #ff2e63; margin-top: 4px; }
}
.content {
  display: flex; gap: 16px;
  .left { flex: 2; }
  .right { flex: 1; line-height: 1.9; color: #606266; font-size: 13px; }
}
.modules {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px;
  .mod {
    background: #fff; padding: 16px; border-radius: 10px; cursor: pointer;
    border: 2px solid transparent; box-shadow: 0 2px 10px rgba(255, 46, 99, .06);
    &.on { border-color: #ff2e63; }
    .mod-title { color: #909399; font-size: 13px; }
    .mod-val { font-size: 20px; font-weight: bold; color: #303133; margin-top: 6px; }
  }
}
</style>