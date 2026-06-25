<template>
  <div>
    <el-row :gutter='20'>
      <el-col :span='6' v-for='(item, index) in statCards' :key='index'>
        <el-card shadow='hover'>
          <div class='stat-value'>{{ item.value }}</div>
          <div class='stat-label'>{{ item.label }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter='20' style='margin-top: 20px;'>
      <el-col :span='12'><el-card><div ref='trendChart' style='height: 300px;'></div></el-card></el-col>
      <el-col :span='12'><el-card><div ref='sourceChart' style='height: 300px;'></div></el-card></el-col>
    </el-row>
    <el-row :gutter='20' style='margin-top: 20px;'>
      <el-col :span='12'><el-card><div ref='stageChart' style='height: 300px;'></div></el-card></el-col>
      <el-col :span='12'><el-card><div ref='rankChart' style='height: 300px;'></div></el-card></el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getStats } from '@/api/dashboard'
export default {
  data() { return { stats: {} } },
  computed: {
    statCards() {
      return [
        { label: '客户总数', value: this.stats.totalCustomers || 0 },
        { label: '商机总数', value: this.stats.totalOpportunities || 0 },
        { label: '订单总数', value: this.stats.totalOrders || 0 },
        { label: '订单金额', value: '¥' + (this.stats.totalAmount || 0) }
      ]
    }
  },
  async mounted() {
    this.stats = await getStats()
    this.initCharts()
  },
  methods: {
    initCharts() {
      const s = this.stats
      echarts.init(this.$refs.trendChart).setOption({
        title: { text: '客户增长趋势' },
        xAxis: { type: 'category', data: (s.customerTrend || []).map(i => i.date) },
        yAxis: { type: 'value' },
        series: [{ data: (s.customerTrend || []).map(i => i.value), type: 'line', smooth: true }]
      })
      echarts.init(this.$refs.sourceChart).setOption({
        title: { text: '客户来源分布' },
        series: [{ type: 'pie', radius: '60%', data: s.sources || [] }]
      })
      echarts.init(this.$refs.stageChart).setOption({
        title: { text: '商机阶段分布' },
        xAxis: { type: 'category', data: (s.stages || []).map(i => i.name) },
        yAxis: { type: 'value' },
        series: [{ data: (s.stages || []).map(i => i.value), type: 'bar' }]
      })
      echarts.init(this.$refs.rankChart).setOption({
        title: { text: '销售排行' },
        xAxis: { type: 'category', data: (s.salesRank || []).map(i => i.name) },
        yAxis: { type: 'value' },
        series: [{ data: (s.salesRank || []).map(i => i.value), type: 'bar' }]
      })
    }
  }
}
</script>

<style scoped>
.stat-value { font-size: 28px; font-weight: bold; color: #303133; }
.stat-label { color: #909399; margin-top: 8px; }
</style>
