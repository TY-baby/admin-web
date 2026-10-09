<template>
  <div>
    <el-alert v-if="hasAlert" :title="alertText" type="error" show-icon :closable="false" class="mb-16" />
    <el-row :gutter="16" class="mb-16">
      <el-col :span="8">
        <el-card shadow="never">
          <div class="gauge-title">CPU 使用率</div>
          <div class="gauge-wrap">
            <el-progress type="dashboard" :percentage="cpu" :color="colorOf(cpu, stats.cpu_threshold)" :width="150" />
          </div>
          <div class="gauge-sub">{{ stats.cpu_count || 0 }} 核 · 阈值 {{ stats.cpu_threshold || 80 }}%</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <div class="gauge-title">内存使用率</div>
          <div class="gauge-wrap">
            <el-progress type="dashboard" :percentage="mem" :color="colorOf(mem, stats.mem_threshold)" :width="150" />
          </div>
          <div class="gauge-sub">{{ gb(stats.mem_used) }} / {{ gb(stats.mem_total) }} · 阈值 {{ stats.mem_threshold || 80 }}%</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <div class="gauge-title">磁盘使用率</div>
          <div class="gauge-wrap">
            <el-progress type="dashboard" :percentage="disk" :color="colorOf(disk, 90)" :width="150" />
          </div>
          <div class="gauge-sub">{{ gb(stats.disk_used) }} / {{ gb(stats.disk_total) }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-card shadow="never">
      <div class="card-title">实时趋势（每 3 秒刷新）</div>
      <line-chart :dates="dates" :series="series" height="340px" />
    </el-card>
  </div>
</template>

<script>
import { getMonitor } from '@/api/adminSystem'
import LineChart from '@/components/LineChart.vue'
export default {
  name: 'AdminMonitor',
  components: { LineChart },
  data() {
    return { stats: {}, dates: [], cpuHist: [], memHist: [], timer: null }
  },
  computed: {
    cpu() { return Number(this.stats.cpu || 0) },
    mem() { return Number(this.stats.mem || 0) },
    disk() { return Number(this.stats.disk || 0) },
    hasAlert() { const a = this.stats.alerts || {}; return !!(a.cpu || a.mem || a.disk) },
    alertText() {
      const a = this.stats.alerts || {}
      const t = []
      if (a.cpu) t.push('CPU 超阈值(' + this.cpu + '%)')
      if (a.mem) t.push('内存超阈值(' + this.mem + '%)')
      if (a.disk) t.push('磁盘超阈值(' + this.disk + '%)')
      return '⚠ 服务器预警：' + t.join('，')
    },
    series() {
      return [
        { name: 'CPU%', data: this.cpuHist, color: '#F56C6C' },
        { name: '内存%', data: this.memHist, color: '#409EFF' }
      ]
    }
  },
  created() { this.fetch(); this.timer = setInterval(this.fetch, 3000) },
  beforeDestroy() { if (this.timer) clearInterval(this.timer) },
  methods: {
    gb(v) { return v ? (v / 1024 / 1024 / 1024).toFixed(1) + ' GB' : '-' },
    colorOf(v, th) {
      const t = th || 80
      return v > t ? '#F56C6C' : (v > t * 0.8 ? '#E6A23C' : '#67C23A')
    },
    async fetch() {
      try {
        const { data } = await getMonitor()
        if (data.code === 0) {
          this.stats = data.data
          const now = new Date().toTimeString().slice(0, 8)
          this.dates.push(now)
          this.cpuHist.push(Number(this.stats.cpu || 0))
          this.memHist.push(Number(this.stats.mem || 0))
          if (this.dates.length > 40) { this.dates.shift(); this.cpuHist.shift(); this.memHist.shift() }
        }
      } catch (e) { /* 忽略轮询异常 */ }
    }
  }
}
</script>

<style scoped lang="scss">
.gauge-title { text-align: center; font-size: 15px; font-weight: bold; color: #0b2a5e; margin-bottom: 10px; }
.gauge-wrap { text-align: center; }
.gauge-sub { text-align: center; color: #909399; font-size: 12px; margin-top: 10px; }
.card-title { font-size: 15px; font-weight: bold; margin-bottom: 12px; border-left: 3px solid #1f6bff; padding-left: 8px; }
</style>