<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <div class="stat-row">
      <div class="stat-card" v-for="(card, i) in statCards" :key="i"
           :style="{ background: card.bg }">
        <div class="stat-card-inner">
          <div class="stat-info">
            <div class="stat-label">{{ card.label }}</div>
            <div class="stat-value">{{ card.prefix }}{{ card.value }}<span class="stat-unit">{{ card.unit }}</span></div>
            <div class="stat-change" :class="card.up ? 'up' : 'down'">
              <i :class="card.up ? 'el-icon-top' : 'el-icon-bottom'"></i>
              {{ card.change }} 较昨日
            </div>
          </div>
          <div class="stat-icon">
            <i :class="card.icon"></i>
          </div>
        </div>
        <div class="stat-footer">
          <span class="stat-footer-label">今日</span>
          <span class="stat-footer-val">{{ card.today }}</span>
        </div>
      </div>
    </div>

    <!-- 图表行 1 -->
    <div class="chart-row">
      <div class="chart-card chart-card-wide">
        <div class="chart-header">
          <div class="chart-title">
            <span class="title-dot" style="background: linear-gradient(135deg,#6366f1,#8b5cf6)"></span>
            销售额趋势
          </div>
          <div class="chart-tabs">
            <span :class="['ctab', {active: salesTab==='week'}]" @click="salesTab='week'">本周</span>
            <span :class="['ctab', {active: salesTab==='month'}]" @click="salesTab='month'">本月</span>
            <span :class="['ctab', {active: salesTab==='year'}]" @click="salesTab='year'">全年</span>
          </div>
        </div>
        <div ref="salesTrendChart" class="chart-body"></div>
      </div>
      <div class="chart-card chart-card-narrow">
        <div class="chart-header">
          <div class="chart-title">
            <span class="title-dot" style="background: linear-gradient(135deg,#ec4899,#f472b6)"></span>
            客户来源分布
          </div>
        </div>
        <div ref="sourceChart" class="chart-body"></div>
      </div>
    </div>

    <!-- 图表行 2 -->
    <div class="chart-row">
      <div class="chart-card chart-card-narrow">
        <div class="chart-header">
          <div class="chart-title">
            <span class="title-dot" style="background: linear-gradient(135deg,#f59e0b,#fbbf24)"></span>
            商机阶段漏斗
          </div>
        </div>
        <div ref="funnelChart" class="chart-body"></div>
      </div>
      <div class="chart-card chart-card-wide">
        <div class="chart-header">
          <div class="chart-title">
            <span class="title-dot" style="background: linear-gradient(135deg,#06b6d4,#22d3ee)"></span>
            销售排行
          </div>
          <div class="chart-tabs">
            <span :class="['ctab', {active: rankTab==='amount'}]" @click="rankTab='amount'">按金额</span>
            <span :class="['ctab', {active: rankTab==='count'}]" @click="rankTab='count'">按单数</span>
          </div>
        </div>
        <div ref="rankChart" class="chart-body"></div>
      </div>
    </div>

    <!-- 图表行 3 -->
    <div class="chart-row">
      <div class="chart-card chart-card-full">
        <div class="chart-header">
          <div class="chart-title">
            <span class="title-dot" style="background: linear-gradient(135deg,#10b981,#34d399)"></span>
            客户增长 & 订单趋势
          </div>
        </div>
        <div ref="comboChart" class="chart-body chart-body-tall"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getStats } from '@/api/dashboard'

export default {
  data() {
    return {
      stats: {},
      salesTab: 'week',
      rankTab: 'amount',
      charts: []
    }
  },
  computed: {
    statCards() {
      const s = this.stats
      return [
        {
          label: '客户总数', value: s.totalCustomers || 0, prefix: '', unit: '人',
          change: '+12.5%', up: true, icon: 'el-icon-user-solid',
          bg: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
          today: '+' + Math.floor(Math.random() * 10 + 3)
        },
        {
          label: '商机总数', value: s.totalOpportunities || 0, prefix: '', unit: '个',
          change: '+8.3%', up: true, icon: 'el-icon-s-flag',
          bg: 'linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%)',
          today: '+' + Math.floor(Math.random() * 5 + 1)
        },
        {
          label: '订单总额', value: s.totalAmount || 0, prefix: '¥', unit: '',
          change: '+15.2%', up: true, icon: 'el-icon-s-order',
          bg: 'linear-gradient(135deg, #ec4899 0%, #f472b6 100%)',
          today: '¥' + Math.floor(Math.random() * 50000 + 10000)
        },
        {
          label: '赢单转化率', value: s.deals ? ((s.deals / Math.max(s.totalOpportunities || 1, 1)) * 100).toFixed(1) : '25.0',
          prefix: '', unit: '%',
          change: '+2.1%', up: true, icon: 'el-icon-trophy',
          bg: 'linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)',
          today: Math.floor(Math.random() * 3 + 1) + '单'
        }
      ]
    }
  },
  watch: {
    salesTab() { this.$nextTick(() => this.initSalesTrend()) },
    rankTab() { this.$nextTick(() => this.initRankChart()) }
  },
  async mounted() {
    try {
      this.stats = await getStats()
    } catch (e) {
      console.warn('获取数据失败，使用默认值', e)
    }
    this.$nextTick(() => {
      this.initSalesTrend()
      this.initSourceChart()
      this.initFunnelChart()
      this.initRankChart()
      this.initComboChart()
    })
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    this.charts.forEach(c => c && c.dispose())
  },
  methods: {
    handleResize() { this.charts.forEach(c => c && c.resize()) },
    makeChart(ref) {
      const chart = echarts.init(this.$refs[ref])
      this.charts.push(chart)
      return chart
    },

    // 销售额趋势 - 柱状图 + 折线图混合
    initSalesTrend() {
      const chart = this.makeChart('salesTrendChart')
      let dates, values, lineValues
      if (this.salesTab === 'week') {
        dates = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        values = [32000, 45000, 38000, 52000, 48000, 61000, 55000]
        lineValues = [28000, 35000, 42000, 46000, 50000, 53000, 49000]
      } else if (this.salesTab === 'month') {
        dates = Array.from({length: 30}, (_, i) => (i + 1) + '日')
        values = dates.map(() => Math.floor(Math.random() * 40000 + 20000))
        lineValues = values.map(v => v * (0.8 + Math.random() * 0.3))
      } else {
        dates = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']
        values = [180000,220000,195000,260000,310000,285000,340000,380000,365000,420000,395000,450000]
        lineValues = [160000,200000,180000,230000,270000,260000,310000,340000,330000,380000,360000,400000]
      }

      // Use actual trend data if available
      if (this.stats.amountTrend && this.stats.amountTrend.length && this.salesTab === 'week') {
        dates = this.stats.amountTrend.map(i => i.date)
        values = this.stats.amountTrend.map(i => i.value * 1000)
        lineValues = values.map(v => v * 0.85)
      }

      chart.setOption({
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(15,23,42,0.9)',
          borderColor: 'rgba(99,102,241,0.3)',
          textStyle: { color: '#e2e8f0' },
          axisPointer: { type: 'shadow', shadowStyle: { color: 'rgba(99,102,241,0.06)' } }
        },
        legend: {
          data: ['本期销售额', '上期销售额'],
          top: 0, right: 0,
          textStyle: { color: '#94a3b8' }
        },
        grid: { top: 40, right: 20, bottom: 30, left: 20, containLabel: true },
        xAxis: {
          type: 'category', data: dates,
          axisLine: { lineStyle: { color: '#334155' } },
          axisLabel: { color: '#94a3b8', fontSize: 11 },
          axisTick: { show: false }
        },
        yAxis: {
          type: 'value',
          splitLine: { lineStyle: { color: '#1e293b', type: 'dashed' } },
          axisLabel: { color: '#94a3b8', fontSize: 11, formatter: v => v >= 10000 ? (v/10000) + 'w' : v },
          axisLine: { show: false }, axisTick: { show: false }
        },
        series: [
          {
            name: '本期销售额', type: 'bar', barWidth: '35%',
            data: values,
            itemStyle: {
              borderRadius: [6, 6, 0, 0],
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#818cf8' },
                { offset: 1, color: '#6366f1' }
              ])
            },
            emphasis: {
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: '#a5b4fc' },
                  { offset: 1, color: '#818cf8' }
                ])
              }
            },
            animationDelay: idx => idx * 80
          },
          {
            name: '上期销售额', type: 'line', smooth: true,
            data: lineValues,
            lineStyle: { color: '#f472b6', width: 2.5, shadowColor: 'rgba(244,114,182,0.4)', shadowBlur: 10 },
            itemStyle: { color: '#f472b6', borderWidth: 2 },
            symbolSize: 6,
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(244,114,182,0.25)' },
                { offset: 1, color: 'rgba(244,114,182,0)' }
              ])
            },
            animationDelay: idx => idx * 80 + 200
          }
        ],
        animationEasing: 'elasticOut',
        animationDuration: 1200
      })
    },

    // 客户来源 - 南丁格尔玫瑰图
    initSourceChart() {
      const chart = this.makeChart('sourceChart')
      const data = (this.stats.sources && this.stats.sources.length) ? this.stats.sources : [
        { name: '官网', value: 35 },
        { name: '推广', value: 28 },
        { name: '转介绍', value: 22 },
        { name: '展会', value: 18 },
        { name: '其他', value: 12 }
      ]
      chart.setOption({
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(15,23,42,0.9)',
          borderColor: 'rgba(236,72,153,0.3)',
          textStyle: { color: '#e2e8f0' },
          formatter: '{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical', right: 10, top: 'center',
          textStyle: { color: '#94a3b8', fontSize: 12 },
          itemWidth: 10, itemHeight: 10, itemGap: 14
        },
        color: ['#6366f1', '#ec4899', '#f59e0b', '#06b6d4', '#10b981', '#8b5cf6', '#f43f5e'],
        series: [{
          type: 'pie',
          radius: ['20%', '70%'],
          center: ['40%', '50%'],
          roseType: 'area',
          label: { show: false },
          emphasis: {
            label: { show: true, fontSize: 14, fontWeight: 'bold', color: '#e2e8f0' },
            itemStyle: { shadowBlur: 20, shadowColor: 'rgba(99,102,241,0.5)' }
          },
          itemStyle: { borderRadius: 6, borderColor: '#0f172a', borderWidth: 2 },
          data: data,
          animationType: 'scale',
          animationEasing: 'elasticOut',
          animationDuration: 1500
        }]
      })
    },

    // 商机阶段 - 漏斗图
    initFunnelChart() {
      const chart = this.makeChart('funnelChart')
      const data = (this.stats.stages && this.stats.stages.length) ? this.stats.stages.map(s => ({ name: s.name, value: s.value })) : [
        { name: '初步接触', value: 45 },
        { name: '需求确认', value: 38 },
        { name: '方案报价', value: 25 },
        { name: '商务谈判', value: 18 },
        { name: '赢单', value: 12 },
        { name: '输单', value: 8 }
      ]
      // Sort by value descending
      data.sort((a, b) => b.value - a.value)

      chart.setOption({
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(15,23,42,0.9)',
          borderColor: 'rgba(245,158,11,0.3)',
          textStyle: { color: '#e2e8f0' },
          formatter: '{b}: {c}'
        },
        color: ['#6366f1', '#818cf8', '#06b6d4', '#f59e0b', '#10b981', '#f43f5e'],
        series: [{
          type: 'funnel',
          left: '10%', width: '80%',
          top: 20, bottom: 20,
          min: 0, max: Math.max(...data.map(d => d.value)),
          minSize: '20%', maxSize: '100%',
          sort: 'descending', gap: 4,
          label: {
            show: true, position: 'inside',
            color: '#fff', fontSize: 12, fontWeight: 'bold',
            formatter: '{b}\n{c}'
          },
          itemStyle: {
            borderColor: 'rgba(15,23,42,0.5)', borderWidth: 1,
            shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.2)'
          },
          emphasis: {
            label: { fontSize: 14 },
            itemStyle: { shadowBlur: 20, shadowColor: 'rgba(99,102,241,0.4)' }
          },
          data: data,
          animationDuration: 1500,
          animationEasing: 'cubicOut'
        }]
      })
    },

    // 销售排行 - 水平柱状图
    initRankChart() {
      const chart = this.makeChart('rankChart')
      const rank = (this.stats.salesRank && this.stats.salesRank.length) ? this.stats.salesRank : [
        { name: '张伟', value: 128 },
        { name: '李娜', value: 105 },
        { name: '王强', value: 88 },
        { name: '刘洋', value: 72 },
        { name: '陈静', value: 65 }
      ]
      const names = rank.map(r => r.name).reverse()
      const values = rank.map(r => r.value).reverse()
      const maxVal = Math.max(...values)

      chart.setOption({
        tooltip: {
          trigger: 'axis', axisPointer: { type: 'shadow' },
          backgroundColor: 'rgba(15,23,42,0.9)',
          borderColor: 'rgba(6,182,212,0.3)',
          textStyle: { color: '#e2e8f0' }
        },
        grid: { top: 10, right: 60, bottom: 10, left: 10, containLabel: true },
        xAxis: {
          type: 'value',
          splitLine: { lineStyle: { color: '#1e293b', type: 'dashed' } },
          axisLabel: { color: '#94a3b8', fontSize: 11 },
          axisLine: { show: false }, axisTick: { show: false }
        },
        yAxis: {
          type: 'category', data: names,
          axisLine: { show: false }, axisTick: { show: false },
          axisLabel: { color: '#e2e8f0', fontSize: 13, fontWeight: 'bold' }
        },
        series: [{
          type: 'bar', barWidth: '50%',
          data: values.map((v, i) => ({
            value: v,
            itemStyle: {
              borderRadius: [0, 6, 6, 0],
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: ['#06b6d4','#6366f1','#ec4899','#f59e0b','#10b981'][i % 5] },
                { offset: 1, color: ['#22d3ee','#818cf8','#f472b6','#fbbf24','#34d399'][i % 5] }
              ])
            }
          })),
          label: {
            show: true, position: 'right', color: '#e2e8f0', fontSize: 12, fontWeight: 'bold',
            formatter: p => {
              const medals = ['🥇','🥈','🥉']
              const idx = values.length - 1 - p.dataIndex
              return (medals[idx] || '') + ' ' + p.value
            }
          },
          emphasis: {
            itemStyle: { shadowBlur: 15, shadowColor: 'rgba(6,182,212,0.4)' }
          },
          animationDelay: idx => idx * 120,
          animationEasing: 'elasticOut',
          animationDuration: 1200
        }]
      })
    },

    // 客户增长 & 订单趋势 - 双Y轴混合图
    initComboChart() {
      const chart = this.makeChart('comboChart')
      let dates
      if (this.stats.customerTrend && this.stats.customerTrend.length) {
        dates = this.stats.customerTrend.map(i => i.date)
      } else {
        dates = Array.from({length: 14}, (_, i) => {
          const d = new Date(); d.setDate(d.getDate() - 13 + i)
          return (d.getMonth()+1) + '/' + d.getDate()
        })
      }
      const customerData = (this.stats.customerTrend || []).length
        ? this.stats.customerTrend.map(i => i.value)
        : dates.map(() => Math.floor(Math.random() * 30 + 10))
      const orderData = (this.stats.orderTrend || []).length
        ? this.stats.orderTrend.map(i => i.value)
        : dates.map(() => Math.floor(Math.random() * 25 + 5))

      chart.setOption({
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(15,23,42,0.9)',
          borderColor: 'rgba(99,102,241,0.3)',
          textStyle: { color: '#e2e8f0' },
          axisPointer: { type: 'cross', crossStyle: { color: '#475569' } }
        },
        legend: {
          data: ['新增客户', '新增订单', '客户增长率'],
          top: 0, textStyle: { color: '#94a3b8' }
        },
        grid: { top: 50, right: 60, bottom: 30, left: 20, containLabel: true },
        xAxis: {
          type: 'category', data: dates,
          axisLine: { lineStyle: { color: '#334155' } },
          axisLabel: { color: '#94a3b8', fontSize: 11 },
          axisTick: { show: false }
        },
        yAxis: [
          {
            type: 'value', name: '数量',
            nameTextStyle: { color: '#94a3b8' },
            splitLine: { lineStyle: { color: '#1e293b', type: 'dashed' } },
            axisLabel: { color: '#94a3b8', fontSize: 11 },
            axisLine: { show: false }, axisTick: { show: false }
          },
          {
            type: 'value', name: '增长率(%)',
            nameTextStyle: { color: '#94a3b8' },
            splitLine: { show: false },
            axisLabel: { color: '#94a3b8', fontSize: 11, formatter: '{value}%' },
            axisLine: { show: false }, axisTick: { show: false }
          }
        ],
        series: [
          {
            name: '新增客户', type: 'bar', barWidth: '30%', barGap: '10%',
            data: customerData,
            itemStyle: {
              borderRadius: [5, 5, 0, 0],
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#818cf8' },
                { offset: 1, color: '#6366f1' }
              ])
            },
            animationDelay: idx => idx * 60
          },
          {
            name: '新增订单', type: 'bar', barWidth: '30%',
            data: orderData,
            itemStyle: {
              borderRadius: [5, 5, 0, 0],
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#34d399' },
                { offset: 1, color: '#10b981' }
              ])
            },
            animationDelay: idx => idx * 60 + 100
          },
          {
            name: '客户增长率', type: 'line', yAxisIndex: 1,
            smooth: true,
            data: customerData.map((v, i, arr) => i === 0 ? 0 : ((v - arr[i-1]) / Math.max(arr[i-1], 1) * 100).toFixed(1)),
            lineStyle: {
              color: '#f59e0b', width: 3,
              shadowColor: 'rgba(245,158,11,0.4)', shadowBlur: 12
            },
            itemStyle: { color: '#f59e0b', borderWidth: 3, borderColor: '#fff' },
            symbolSize: 8,
            symbol: 'circle',
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(245,158,11,0.2)' },
                { offset: 1, color: 'rgba(245,158,11,0)' }
              ])
            },
            animationDelay: idx => idx * 60 + 300
          }
        ],
        animationEasing: 'elasticOut',
        animationDuration: 1500
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  padding: 0;
  background: #0f172a;
  min-height: calc(100vh - 120px);
}

/* 统计卡片 */
.stat-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 16px;
  padding: 24px;
  color: #fff;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 4px 24px rgba(0,0,0,0.2);

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
  }

  &::after {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 120px; height: 120px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
  }
}

.stat-card-inner {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.stat-info { flex: 1; }

.stat-label {
  font-size: 13px;
  opacity: 0.85;
  margin-bottom: 8px;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.5px;
}

.stat-unit {
  font-size: 14px;
  font-weight: 400;
  opacity: 0.7;
  margin-left: 4px;
}

.stat-change {
  margin-top: 8px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 2px;
  opacity: 0.9;

  &.up { color: rgba(255,255,255,0.9); }
  &.down { color: rgba(255,255,255,0.9); }
}

.stat-icon {
  width: 52px; height: 52px;
  background: rgba(255,255,255,0.15);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  backdrop-filter: blur(10px);
}

.stat-footer {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid rgba(255,255,255,0.15);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  opacity: 0.8;
}

/* 图表区域 */
.chart-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
  border: 1px solid #1e3a5f;
  border-radius: 16px;
  padding: 20px;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #ec4899, #06b6d4);
    border-radius: 16px 16px 0 0;
  }
}

.chart-card-wide { flex: 1.6; }
.chart-card-narrow { flex: 1; }
.chart-card-full { flex: 1; }

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.chart-title {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  display: inline-block;
  box-shadow: 0 0 8px currentColor;
}

.chart-tabs {
  display: flex;
  gap: 4px;
  background: rgba(255,255,255,0.05);
  border-radius: 8px;
  padding: 3px;
}

.ctab {
  padding: 5px 14px;
  border-radius: 6px;
  font-size: 12px;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.25s ease;

  &:hover { color: #e2e8f0; }

  &.active {
    background: linear-gradient(135deg, #6366f1, #818cf8);
    color: #fff;
    box-shadow: 0 2px 8px rgba(99,102,241,0.4);
  }
}

.chart-body {
  height: 320px;
}

.chart-body-tall {
  height: 350px;
}
</style>
