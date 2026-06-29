<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">系统监控</div>
      <div class="hero-desc">实时查看 CPU、内存、磁盘、网络与操作系统等运行状态，并展示资源使用趋势。</div>
    </div>

    <div class="plate-card" style="margin-bottom:20px">
      <div class="plate-toolbar">
        <div class="plate-actions">
          <el-button icon="el-icon-refresh" :loading="loading" @click="load">立即刷新</el-button>
          <el-select v-model="interval" placeholder="刷新间隔" style="width:140px" @change="setTimer">
            <el-option label="5 秒" :value="5" />
            <el-option label="10 秒" :value="10" />
            <el-option label="30 秒" :value="30" />
            <el-option label="关闭" :value="0" />
          </el-select>
        </div>
      </div>
      <div class="plate-grid-4">
        <div class="metric-card" v-for="(m, i) in metrics" :key="i">
          <div class="metric-icon"><i :class="m.icon"></i></div>
          <div class="metric-info">
            <div class="metric-label">{{ m.label }}</div>
            <div class="metric-value">{{ m.value }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="plate-grid-3">
      <div class="plate-card">
        <div class="card-title">CPU 使用率趋势</div>
        <svg class="sparkline" viewBox="0 0 300 120" preserveAspectRatio="none">
          <path :d="cpuPath" fill="none" stroke="#3b82f6" stroke-width="2" />
        </svg>
      </div>
      <div class="plate-card">
        <div class="card-title">内存使用趋势</div>
        <svg class="sparkline" viewBox="0 0 300 120" preserveAspectRatio="none">
          <path :d="memPath" fill="none" stroke="#10b981" stroke-width="2" />
        </svg>
      </div>
      <div class="plate-card">
        <div class="card-title">磁盘使用趋势</div>
        <svg class="sparkline" viewBox="0 0 300 120" preserveAspectRatio="none">
          <path :d="diskPath" fill="none" stroke="#f59e0b" stroke-width="2" />
        </svg>
      </div>
    </div>
  </div>
</template>

<script>
import { getSystemMonitor } from '@/api/modules/plate'
import { formatSize, formatPercent, handleReq, buildLinePath } from './helpers'

export default {
  data() {
    return {
      loading: false,
      monitor: {},
      interval: 5,
      timer: null,
      history: { cpu: [], mem: [], disk: [] }
    }
  },
  computed: {
    metrics() {
      const m = this.monitor
      return [
        { label: 'CPU 使用率', value: formatPercent(m.cpu_percent), icon: 'el-icon-cpu' },
        { label: '内存占用', value: formatPercent(m.memory_percent), icon: 'el-icon-monitor' },
        { label: '磁盘占用', value: formatPercent(m.disk_percent), icon: 'el-icon-receiving' },
        { label: '网络收发', value: (m.net_sent ? formatSize(m.net_sent) + '/' + formatSize(m.net_recv) : '-'), icon: 'el-icon-sort' }
      ]
    },
    cpuPath() {
      return buildLinePath(this.history.cpu, 300, 120, 0, 100)
    },
    memPath() {
      return buildLinePath(this.history.mem, 300, 120, 0, 100)
    },
    diskPath() {
      return buildLinePath(this.history.disk, 300, 120, 0, 100)
    }
  },
  created() { this.load(); this.setTimer() },
  beforeDestroy() { clearInterval(this.timer) },
  methods: {
    formatSize, formatPercent,
    async load() {
      this.loading = true
      try {
        this.monitor = await handleReq(getSystemMonitor())
        this.history.cpu.push((this.monitor.cpu_percent || 0) * 100)
        this.history.mem.push((this.monitor.memory_percent || 0) * 100)
        this.history.disk.push((this.monitor.disk_percent || 0) * 100)
        if (this.history.cpu.length > 30) {
          this.history.cpu.shift()
          this.history.mem.shift()
          this.history.disk.shift()
        }
      } finally {
        this.loading = false
      }
    },
    setTimer() {
      clearInterval(this.timer)
      if (this.interval > 0) {
        this.timer = setInterval(() => this.load(), this.interval * 1000)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
.metric-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px;
}
.metric-icon {
  width: 48px; height: 48px; border-radius: 12px;
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  color: #fff; display: flex; align-items: center; justify-content: center; font-size: 22px;
}
.metric-info { flex: 1; }
.metric-label { font-size: 13px; color: #64748b; margin-bottom: 6px; }
.metric-value { font-size: 22px; font-weight: 800; color: #1e293b; }
.card-title { font-size: 16px; font-weight: 700; margin-bottom: 16px; }
.sparkline { width: 100%; height: 120px; }
</style>
