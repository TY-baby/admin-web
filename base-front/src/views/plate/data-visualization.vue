<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">数据可视化大屏</div>
      <div class="hero-desc">全局展示图片、视频、检测次数、结果分布与近期识别记录等核心业务态势。</div>
    </div>

    <div class="plate-stat-row">
      <div class="plate-stat-card" v-for="(s, i) in statCards" :key="i">
        <div class="stat-label">{{ s.label }}</div>
        <div class="stat-value">{{ s.value }}</div>
      </div>
    </div>

    <div class="plate-grid-2">
      <div class="plate-card">
        <div class="card-title">检测结果分布</div>
        <div ref="pieChart" class="chart-box"></div>
      </div>
      <div class="plate-card">
        <div class="card-title">近 7 天检测趋势</div>
        <div ref="lineChart" class="chart-box"></div>
      </div>
    </div>

    <div class="plate-grid-2" style="margin-top:20px">
      <div class="plate-card">
        <div class="card-title">车牌统计 TOP</div>
        <el-table :data="plateStats" border>
          <el-table-column prop="plate_no" label="车牌号" />
          <el-table-column prop="count" label="识别次数" width="120" />
        </el-table>
      </div>
      <div class="plate-card">
        <div class="card-title">近期检测记录</div>
        <el-table :data="recentRecords" border>
          <el-table-column prop="filename" label="文件名" />
          <el-table-column prop="type" label="类型" width="80" />
          <el-table-column prop="create_time" label="时间" width="160">
            <template slot-scope="scope">{{ formatDate(scope.row.create_time) }}</template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getDashboardStats, getRecentRecords } from '@/api/modules/plate'
import { formatDate, handleReq } from './helpers'

export default {
  data() {
    return {
      stats: {},
      plateStats: [],
      recentRecords: [],
      charts: []
    }
  },
  computed: {
    statCards() {
      const s = this.stats
      return [
        { label: '图片总数', value: s.imageCount || 0 },
        { label: '视频总数', value: s.videoCount || 0 },
        { label: '检测总次数', value: s.detectCount || 0 },
        { label: '检测记录总数', value: s.recordCount || 0 }
      ]
    }
  },
  async mounted() {
    try {
      this.stats = await handleReq(getDashboardStats())
      this.plateStats = this.stats.plateStats || []
      this.recentRecords = await handleReq(getRecentRecords({ limit: 10 }))
    } catch (e) {
      console.warn('加载数据失败', e)
    }
    this.$nextTick(() => {
      this.initPie()
      this.initLine()
    })
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    this.charts.forEach(c => c && c.dispose())
  },
  methods: {
    formatDate,
    handleResize() { this.charts.forEach(c => c && c.resize()) },
    makeChart(ref) {
      const chart = echarts.init(this.$refs[ref])
      this.charts.push(chart)
      return chart
    },
    initPie() {
      const data = this.stats.resultDistribution || [
        { name: '蓝牌', value: 35 },
        { name: '黄牌', value: 22 },
        { name: '绿牌', value: 18 },
        { name: '白牌', value: 12 },
        { name: '其他', value: 8 }
      ]
      this.makeChart('pieChart').setOption({
        tooltip: { trigger: 'item' },
        legend: { bottom: 0, textStyle: { color: '#64748b' } },
        color: ['#3b82f6', '#f59e0b', '#10b981', '#94a3b8', '#6366f1'],
        series: [{
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['50%', '45%'],
          itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
          label: { color: '#475569' },
          data
        }]
      })
    },
    initLine() {
      const data = this.stats.trend || []
      const dates = data.length ? data.map(i => i.date) : Array.from({ length: 7 }, (_, i) => {
        const d = new Date(); d.setDate(d.getDate() - 6 + i)
        return (d.getMonth() + 1) + '/' + d.getDate()
      })
      const values = data.length ? data.map(i => i.value) : [12, 19, 15, 22, 28, 24, 32]
      this.makeChart('lineChart').setOption({
        tooltip: { trigger: 'axis' },
        grid: { top: 20, right: 20, bottom: 30, left: 20, containLabel: true },
        xAxis: { type: 'category', data: dates, axisLine: { lineStyle: { color: '#cbd5e1' } }, axisLabel: { color: '#64748b' } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#e2e8f0', type: 'dashed' } }, axisLabel: { color: '#64748b' } },
        series: [{
          data: values,
          type: 'line',
          smooth: true,
          lineStyle: { color: '#3b82f6', width: 3 },
          areaStyle: { color: 'rgba(59,130,246,0.15)' },
          itemStyle: { color: '#3b82f6' }
        }]
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
.card-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
}
.chart-box {
  height: 280px;
}
</style>
