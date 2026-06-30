<template>
  <div class="erp-page">
    <div class="erp-header">
      <div class="erp-title">ERP 概览</div>
      <div class="erp-desc">企业资源计划核心指标一览</div>
    </div>

    <div class="erp-stat-grid">
      <div class="erp-stat-card" v-for="(s, i) in stats" :key="i">
        <div class="stat-icon"><i :class="s.icon"></i></div>
        <div class="stat-info">
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </div>

    <div class="erp-card">
      <div class="card-title">本月业务趋势</div>
      <div ref="chart" class="chart-area"></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      stats: [
        { label: '采购订单', value: '128', icon: 'el-icon-s-order' },
        { label: '库存总量', value: '36,520', icon: 'el-icon-s-goods' },
        { label: '在制工单', value: '45', icon: 'el-icon-s-tools' },
        { label: '销售金额', value: '¥ 892,400', icon: 'el-icon-s-data' },
        { label: '应付账款', value: '¥ 234,000', icon: 'el-icon-s-finance' },
        { label: '在职员工', value: '86', icon: 'el-icon-user' }
      ]
    }
  },
  mounted() {
    this.initChart()
  },
  methods: {
    initChart() {
      const echarts = require('echarts')
      const chart = echarts.init(this.$refs.chart)
      chart.setOption({
        tooltip: { trigger: 'axis' },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'category', data: ['1日', '5日', '10日', '15日', '20日', '25日', '30日'] },
        yAxis: { type: 'value' },
        series: [
          { name: '采购', type: 'line', smooth: true, data: [120, 132, 101, 134, 90, 230, 210] },
          { name: '销售', type: 'line', smooth: true, data: [220, 182, 191, 234, 290, 330, 310] },
          { name: '库存', type: 'bar', data: [150, 232, 201, 154, 190, 330, 410] }
        ]
      })
      window.addEventListener('resize', () => chart.resize())
    }
  }
}
</script>

<style lang="scss" scoped>
.erp-page { padding: 20px; }
.erp-header {
  background: linear-gradient(135deg, #4f46e5, #818cf8);
  border-radius: 12px;
  padding: 24px;
  color: #fff;
  margin-bottom: 20px;
}
.erp-title { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.erp-desc { font-size: 14px; opacity: 0.9; }
.erp-stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}
.erp-stat-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.stat-icon {
  width: 48px; height: 48px;
  border-radius: 10px;
  background: #eef2ff;
  color: #4f46e5;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
}
.stat-value { font-size: 22px; font-weight: 700; color: #1e293b; }
.stat-label { font-size: 13px; color: #64748b; margin-top: 4px; }
.erp-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.card-title { font-size: 16px; font-weight: 700; margin-bottom: 16px; color: #1e293b; }
.chart-area { width: 100%; height: 360px; }
</style>
