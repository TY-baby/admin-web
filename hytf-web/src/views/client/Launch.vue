<template>
  <div class="client-sub">
    <div class="topbar flex-between">
      <div class="logo" @click="$router.push('/client/home')" style="cursor:pointer">恒耀互娱 - 流水明细</div>
      <div class="nav">
        <router-link to="/client/home" class="nav-item">首页</router-link>
        <router-link to="/client/finance" class="nav-item">财务</router-link>
        <router-link to="/client/launch" class="nav-item active">流水明细</router-link>
      </div>
    </div>
    <div class="page-container">
      <div class="summary card">
        <div class="customer-hero">
          <i class="el-icon-user-solid hero-ico"></i>
          <div class="hero-txt">
            <div class="hero-name">{{ info.customer_name || '未命名客户' }}</div>
            <div class="hero-phone"><i class="el-icon-mobile-phone"></i> {{ info.phone || '-' }}</div>
          </div>
        </div>
        <div class="flex-between">
          <div><div class="lbl">账号总余额</div><div class="big">￥{{ summary.total_balance || 0 }}</div></div>
          <div><div class="lbl">累计消费</div><div class="big">￥{{ summary.total_consume || 0 }}</div></div>
          <div><div class="lbl">ID总数</div><div class="big">{{ summary.account_count || 0 }}</div></div>
        </div>
      </div>

      <div class="filter card">
        <span style="margin-right:8px">日期</span>
        <el-date-picker v-model="range" type="daterange" value-format="yyyy-MM-dd"
                        start-placeholder="开始" end-placeholder="结束" :clearable="false"
                        :picker-options="pickerOptions" />
        <el-select v-model="launchType" placeholder="请选择类型" style="margin-left:12px;width:150px">
          <el-option label="首充" value="FIRST_CHARGE" />
          <el-option label="直播曝光度" value="EXPOSURE" />
        </el-select>
        <el-cascader v-model="cascade" :options="cascadeOptions" :props="cascaderProps"
                     placeholder="平台 / ID" clearable filterable
                     style="margin-left:12px;width:280px" />
        <el-button type="primary" icon="el-icon-search" style="margin-left:8px" @click="loadTrend">查询</el-button>
        <el-button type="danger" icon="el-icon-download" style="margin-left:8px" @click="onExport">导出Excel</el-button>
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
            <line-chart :dates="dates" :series="series" :y-min="yBounds.min" :y-max="yBounds.max"
                        :smooth="false" :area="false" point-label height="360px" />
          </div>
        </div>
        <div class="right card">
          <div class="card-title">日常方案</div>
          <p>1. 建议每日固定时间查看投放数据，保持投放节奏稳定。</p>
          <p>2. 首次投放推荐使用 A 档位，观察 3 天效果后再调整。</p>
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
import { getSummary, getTrend, getPlatforms, clientExportUrl } from '@/api/clientHome'
import { getClientToken } from '@/utils/auth'
import LineChart from '@/components/LineChart.vue'

export default {
  name: 'ClientLaunch',
  components: { LineChart },
  data() {
    const y = new Date(Date.now() - 86400000).toISOString().slice(0, 10)
    return {
      summary: {}, range: [y, y], launchType: '', cascade: [],
      platforms: [], activeMod: 'consume', dates: [], series: [], raw: [], stats: null,
      pickerOptions: { disabledDate(t) { return t.getTime() > Date.now() - 86400000 } },
      cascaderProps: { value: 'value', label: 'label', children: 'children' }
    }
  },
  computed: {
    ...mapState('clientUser', ['accounts', 'info']),
    cascadeOptions() {
      const groups = {}
      ;(this.accounts || []).forEach(a => {
        const p = this.platforms.find(x => x.code === a.platform_code)
        const pname = p ? p.name : a.platform_code
        if (!groups[a.platform_code]) groups[a.platform_code] = { value: a.platform_code, label: pname, children: [] }
        groups[a.platform_code].children.push({
          value: a.id,
          label: a.douyin_id + (a.douyin_name ? '（' + a.douyin_name + '）' : '')
        })
      })
      return Object.values(groups)
    },
    accountId() { return this.cascade && this.cascade.length === 2 ? this.cascade[1] : '' },
    yBounds() {
      const data = ((this.series[0] && this.series[0].data) || []).map(Number)
      const dataMax = data.length ? Math.max(...data) : 0
      return { min: 0, max: dataMax || null }
    },
    modules() {
      const sum = k => (this.raw || []).reduce((s, x) => s + Number(x[k] || 0), 0).toFixed(2)
      const totalConsume = sum('consume')
      const avg = this.raw.length ? (Number(totalConsume) / this.raw.length).toFixed(2) : '0.00'
      const list = [
        { key: 'consume', title: '总消费', value: '￥' + totalConsume },
        { key: 'avg', title: '日均消费', value: '￥' + avg }
      ]
      if (this.launchType === 'FIRST_CHARGE' && this.stats) {
        list.push({ key: 'first_amount', title: '首充金额', value: '￥' + Number(this.stats.first_amount || 0).toFixed(2) })
        list.push({ key: 'first_count', title: '首充ID数', value: this.stats.first_count || 0 })
      }
      if (this.launchType === 'EXPOSURE' && this.stats) {
        list.push({ key: 'heat', title: '热度', value: this.stats.heat_total || 0 })
      }
      return list
    }
  },
  async created() {
    if (!this.accounts.length) await this.$store.dispatch('clientUser/loadAccounts')
    const [{ data: pd }, { data: sd }] = await Promise.all([getPlatforms(), getSummary()])
    if (pd.code === 0) this.platforms = pd.data || []
    if (sd.code === 0) this.summary = sd.data
    // 2.3：初始化不查询
  },
  methods: {
    validate() {
      if (!this.launchType) { this.$message.warning('请选择类型（首充/直播曝光度）'); return false }
      if (!this.accountId) { this.$message.warning('请选择平台和ID'); return false }
      if (!this.range || this.range.length !== 2) { this.$message.warning('请选择日期'); return false }
      return true
    },
    async loadTrend() {
      if (!this.validate()) return
      const params = { start: this.range[0], end: this.range[1],
                       account_id: this.accountId, launch_type: this.launchType }
      const { data } = await getTrend(params)
      if (data.code === 0) {
        this.raw = data.data.items || []
        this.stats = data.data.stats || null
        this.dates = this.raw.map(x => x.date)
        this.applySeries()
      }
    },
    selectMod(k) { this.activeMod = k; this.applySeries() },
    onExport() {
      if (!this.validate()) return
      const q = new URLSearchParams()
      q.append('start', this.range[0])
      q.append('end', this.range[1])
      q.append('account_id', this.accountId)
      q.append('launch_type', this.launchType)
      fetch(clientExportUrl + '?' + q.toString(),
            { headers: { Authorization: 'Bearer ' + getClientToken() } })
        .then(async r => {
          const ct = r.headers.get('content-type') || ''
          if (ct.indexOf('json') !== -1) {
            const j = await r.json(); this.$message.error(j.msg || '导出失败'); return null
          }
          return r.blob()
        })
        .then(b => {
          if (!b) return
          const a = document.createElement('a')
          a.href = URL.createObjectURL(b)
          const typeLabel = this.launchType === 'EXPOSURE' ? '直播曝光度' : '首充'
          a.download = `流水明细_${typeLabel}_${this.range[0]}_${this.range[1]}.xlsx`
          a.click()
          URL.revokeObjectURL(a.href)
          this.$message.success('导出成功')
        }).catch(() => this.$message.error('导出失败'))
    },
    applySeries() {
      const key = this.activeMod
      const nameMap = { consume: '消费', avg: '日均消费', first_amount: '首充金额', first_count: '首充ID数', heat: '热度' }
      const colorMap = { consume: '#F56C6C', avg: '#E6A23C', first_amount: '#67C23A', first_count: '#409EFF', heat: '#FF9800' }
      if (key === 'avg') {
        const total = (this.raw || []).reduce((s, x) => s + Number(x.consume || 0), 0)
        const avg = this.raw.length ? total / this.raw.length : 0
        this.series = [{ name: nameMap[key], data: this.raw.map(() => Number(avg.toFixed(2))), color: colorMap[key] }]
      } else if (key === 'consume') {
        this.series = [{ name: nameMap[key], data: this.raw.map(x => Number(x[key] || 0)), color: colorMap[key] }]
      } else {
        // 首充金额/首充ID数/热度 是区间累加值，展示为水平线
        const v = this.stats ? Number(this.stats[key === 'heat' ? 'heat_total' : key] || 0) : 0
        this.series = [{ name: nameMap[key], data: this.raw.map(() => v), color: colorMap[key] }]
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
  display: flex; justify-content: space-between; align-items: center;
  .logo { font-weight: bold; font-size: 18px; color: #fff; }
  .nav-item { margin: 0 12px; color: rgba(255,255,255,.85); font-size: 14px;
    &.active { color: #fff; font-weight: bold; border-bottom: 2px solid #fff; } }
  ::v-deep .el-button--text { color: #fff; }
}
.card { background: #fff; border-radius: 12px; padding: 18px; margin-bottom: 16px;
  box-shadow: 0 4px 16px rgba(255, 46, 99, .08);
  .card-title { font-size: 15px; font-weight: bold; margin-bottom: 12px;
    border-left: 3px solid #ff2e63; padding-left: 8px; } }
.summary { .lbl { color: #909399; font-size: 13px; }
  .big { font-size: 22px; font-weight: bold; color: #ff2e63; margin-top: 4px; } }
.customer-hero { display: flex; align-items: center; gap: 14px;
  padding: 12px 18px; margin-bottom: 14px;
  background: linear-gradient(120deg, #ff5f8f 0%, #ff2e63 100%);
  border-radius: 10px; box-shadow: 0 4px 14px rgba(255, 46, 99, .28);
  .hero-ico { font-size: 32px; color: #fff; }
  .hero-txt { color: #fff; }
  .hero-name { font-size: 20px; font-weight: 800; letter-spacing: 1px; line-height: 1.2; }
  .hero-phone { font-size: 14px; margin-top: 4px; opacity: .95; i { margin-right: 4px; } } }
.content { display: flex; gap: 16px;
  .left { flex: 2; } .right { flex: 1; line-height: 1.9; color: #606266; font-size: 13px; } }
.modules { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px;
  .mod { background: #fff; padding: 16px; border-radius: 10px; cursor: pointer;
    border: 2px solid transparent; box-shadow: 0 2px 10px rgba(255, 46, 99, .06);
    &.on { border-color: #ff2e63; }
    .mod-title { color: #909399; font-size: 13px; }
    .mod-val { font-size: 20px; font-weight: bold; color: #303133; margin-top: 6px; } } }
</style>