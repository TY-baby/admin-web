<template>
  <screen-wrapper title="销售轮播大屏">
    <div class="sales-screen">
      <div class="sales-welcome">
        <h2>智慧大屏展示中心</h2>
        <p>本菜单组聚合了多套行业数据可视化大屏，点击左侧菜单可切换不同主题大屏，数据均为模拟数据。</p>
        <el-button type="primary" size="medium" @click="$router.push('/bigscreen/fullscreen')">
          <i class="el-icon-full-screen"></i> 进入全屏轮播
        </el-button>
      </div>

      <div class="screen-cards">
        <div class="screen-card" v-for="(s, i) in screens" :key="i" @click="$router.push(s.path)">
          <div class="card-thumb" :style="{background: s.gradient}">
            <i :class="s.icon"></i>
          </div>
          <div class="card-info">
            <div class="card-title">{{ s.title }}</div>
            <div class="card-desc">{{ s.desc }}</div>
          </div>
        </div>
      </div>

      <div class="sales-charts">
        <screen-panel title="本月销售趋势" class="trend-panel">
          <div ref="trendChart" class="chart-box"></div>
        </screen-panel>
        <screen-panel title="产品占比" class="pie-panel">
          <div ref="pieChart" class="chart-box"></div>
        </screen-panel>
      </div>
    </div>
  </screen-wrapper>
</template>

<script>
import * as echarts from 'echarts'
import ScreenWrapper from '../components/ScreenWrapper.vue'
import ScreenPanel from '../components/ScreenPanel.vue'

export default {
  components: { ScreenWrapper, ScreenPanel },
  data() {
    return {
      screens: [
        { title: '异常管理驾驶舱', desc: '产线异常、报警、排行与趋势', path: '/bigscreen/abnormal', icon: 'el-icon-warning-outline', gradient: 'linear-gradient(135deg, #f87171, #ef4444)' },
        { title: '化工生产监控', desc: 'PVC产量、库存、销量与价格', path: '/bigscreen/chemical', icon: 'el-icon-s-data', gradient: 'linear-gradient(135deg, #00d4ff, #0ea5e9)' },
        { title: '销售业绩看板', desc: '业务员排名、大区销售、趋势', path: '/bigscreen/sales-rank', icon: 'el-icon-trophy', gradient: 'linear-gradient(135deg, #fbbf24, #d97706)' },
        { title: '航空运营监控', desc: '航班、准点率、延误与地面保障', path: '/bigscreen/aviation', icon: 'el-icon-s-promotion', gradient: 'linear-gradient(135deg, #60a5fa, #3b82f6)' },
        { title: '园区HSE监控', desc: '隐患、作业票、环保指标监控', path: '/bigscreen/hse', icon: 'el-icon-warning', gradient: 'linear-gradient(135deg, #34d399, #059669)' }
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initTrendChart()
      this.initPieChart()
    })
  },
  methods: {
    initTrendChart() {
      const chart = echarts.init(this.$refs.trendChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        grid: { top: 30, right: 20, bottom: 25, left: 40, containLabel: true },
        xAxis: { type: 'category', data: ['1日','5日','10日','15日','20日','25日','30日'], axisLabel: { color: '#6b8ab5' }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5' } },
        series: [
          { type: 'line', smooth: true, data: [120, 180, 150, 220, 260, 210, 290], lineStyle: { color: '#00d4ff', width: 3 }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(0,212,255,0.25)'},{offset:1,color:'rgba(0,212,255,0)'}] } }, itemStyle: { color: '#00d4ff' } }
        ]
      })
    },
    initPieChart() {
      const chart = echarts.init(this.$refs.pieChart)
      chart.setOption({
        tooltip: { trigger: 'item', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        legend: { orient: 'vertical', right: 0, top: 'center', textStyle: { color: '#6b8ab5' } },
        series: [{
          type: 'pie', radius: ['45%', '70%'], center: ['35%', '50%'], label: { color: '#e2e8f0' },
          data: [
            { value: 320, name: 'PVC', itemStyle: { color: '#00d4ff' } },
            { value: 240, name: '烧碱', itemStyle: { color: '#fbbf24' } },
            { value: 180, name: '盐酸', itemStyle: { color: '#f87171' } },
            { value: 260, name: '水泥', itemStyle: { color: '#34d399' } }
          ]
        }]
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.sales-screen { display: flex; flex-direction: column; gap: 14px; height: 100%; }
.sales-welcome {
  background: linear-gradient(135deg, rgba(12,26,58,0.85), rgba(8,18,46,0.95));
  border: 1px solid rgba(0,212,255,0.12);
  border-radius: 12px;
  padding: 18px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sales-welcome h2 { margin: 0; font-size: 18px; color: #e2e8f0; }
.sales-welcome p { margin: 6px 0 0; font-size: 12px; color: #6b8ab5; }

.screen-cards { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }
.screen-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 12px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s;
  &:hover { transform: translateY(-3px); border-color: rgba(0,212,255,0.2); }
}
.card-thumb { width: 48px; height: 48px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 22px; }
.card-title { font-size: 14px; font-weight: 600; color: #e2e8f0; }
.card-desc { font-size: 11px; color: #6b8ab5; margin-top: 4px; }

.sales-charts { flex: 1; display: flex; gap: 14px; min-height: 0; }
.trend-panel { flex: 1.5; min-width: 0; }
.pie-panel { flex: 1; min-width: 0; }
.chart-box { width: 100%; height: 100%; }
</style>
