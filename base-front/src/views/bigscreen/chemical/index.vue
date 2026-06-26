<template>
  <screen-wrapper title="化工生产监控">
    <div class="chemical-screen">
      <div class="row row-main">
        <!-- 左侧 -->
        <div class="left-col">
          <screen-panel title="产品产量与完成率">
            <table class="data-table">
              <thead><tr><th>产品</th><th>日产量</th><th>月产量</th><th>月计划完成率</th></tr></thead>
              <tbody>
                <tr v-for="(p, i) in products" :key="i">
                  <td>{{ p.name }}</td><td>{{ p.daily }}</td><td>{{ p.monthly }}</td>
                  <td><span class="progress-bar"><span :style="{width: p.rate}"></span></span>{{ p.rate }}</td>
                </tr>
              </tbody>
            </table>
            <div class="rate-cards">
              <div class="rate-card" v-for="(r, i) in rates" :key="i">
                <div class="rate-value" :style="{color: r.color}">{{ r.value }}</div>
                <div class="rate-name">{{ r.name }}</div>
              </div>
            </div>
          </screen-panel>

          <screen-panel title="原料库存" height="240px">
            <div ref="stockChart" class="chart-box"></div>
          </screen-panel>

          <screen-panel title="产品库存" height="240px">
            <div ref="productStockChart" class="chart-box"></div>
          </screen-panel>
        </div>

        <!-- 中间 -->
        <div class="center-col">
          <screen-panel title="PVC销量分布" class="map-panel">
            <div class="map-stats">
              <div class="map-stat"><span>应收额</span><strong style="color:#f87171">410500</strong></div>
              <div class="map-stat"><span>信用额</span><strong style="color:#fbbf24">435000</strong></div>
            </div>
            <div ref="mapChart" class="chart-box map-box"></div>
            <div class="map-legend">
              <span><i class="dot low"></i>低</span>
              <span><i class="dot mid"></i>中</span>
              <span><i class="dot high"></i>高</span>
            </div>
          </screen-panel>

          <screen-panel title="产品销售">
            <div ref="salesChart" class="chart-box"></div>
          </screen-panel>
        </div>

        <!-- 右侧 -->
        <div class="right-col">
          <screen-panel title="应收账款分析">
            <div class="account-cards">
              <div class="account-card" v-for="(a, i) in accounts" :key="i">
                <div class="account-title">{{ a.title }}</div>
                <div class="account-grid">
                  <div><span>应收额</span><strong>{{ a.receivable }}</strong></div>
                  <div><span>信用额</span><strong>{{ a.credit }}</strong></div>
                </div>
              </div>
            </div>
            <div class="ring-row">
              <div class="ring-box" v-for="(r, i) in rings" :key="i">
                <div ref="ringChart" class="mini-ring" :id="'ring-'+i"></div>
                <div class="ring-label">{{ r.label }}</div>
              </div>
            </div>
          </screen-panel>

          <screen-panel title="原盐单价">
            <div ref="saltChart" class="chart-box"></div>
          </screen-panel>

          <screen-panel title="煤炭单价">
            <div ref="coalChart" class="chart-box"></div>
          </screen-panel>

          <screen-panel title="石灰石单价">
            <div ref="limeChart" class="chart-box"></div>
          </screen-panel>
        </div>
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
      products: [
        { name: 'PVC', daily: 20, monthly: 632, rate: '88%' },
        { name: '烧碱', daily: 18, monthly: 589, rate: '91%' },
        { name: '盐酸', daily: 19, monthly: 604, rate: '89%' },
        { name: '水泥', daily: 21, monthly: 628, rate: '94%' }
      ],
      rates: [
        { name: 'PVC完成率', value: '88%', color: '#34d399' },
        { name: '烧碱完成率', value: '91%', color: '#fbbf24' },
        { name: '盐酸完成率', value: '89%', color: '#60a5fa' },
        { name: '水泥完成率', value: '94%', color: '#f87171' }
      ],
      accounts: [
        { title: '化工', receivable: 125500, credit: 150000 },
        { title: '热电', receivable: 150000, credit: 145000 },
        { title: '水泥', receivable: 135000, credit: 140000 }
      ],
      rings: [
        { label: '化工', in: 87, out: 13 },
        { label: '热电', in: 89, out: 11 },
        { label: '水泥', in: 92, out: 8 }
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initStockChart()
      this.initProductStockChart()
      this.initMapChart()
      this.initSalesChart()
      this.initRings()
      this.initLineChart(this.$refs.saltChart, '#f472b6')
      this.initLineChart(this.$refs.coalChart, '#fbbf24')
      this.initLineChart(this.$refs.limeChart, '#34d399')
    })
  },
  methods: {
    chartTheme() {
      return { axisLine: '#2a3a5e', axisLabel: '#6b8ab5', splitLine: '#1a2744', tooltipBg: 'rgba(8,18,46,0.95)', tooltipBorder: '#1e3a5f' }
    },
    initStockChart() {
      const chart = echarts.init(this.$refs.stockChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        legend: { data: ['30天内', '30天外'], top: 0, textStyle: { color: '#6b8ab5' } },
        grid: { top: 30, right: 10, bottom: 20, left: 30, containLabel: true },
        xAxis: { type: 'category', data: ['电石', '原煤', '原盐'], axisLabel: { color: '#6b8ab5' }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5' } },
        series: [
          { name: '30天内', type: 'bar', stack: 'total', data: [12, 28, 17], itemStyle: { color: '#fbbf24', borderRadius: [0,0,4,4] }, barWidth: '40%' },
          { name: '30天外', type: 'bar', stack: 'total', data: [5, 7, 22], itemStyle: { color: '#f87171', borderRadius: [4,4,0,0] }, barWidth: '40%' }
        ]
      })
    },
    initProductStockChart() {
      const chart = echarts.init(this.$refs.productStockChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        legend: { data: ['30天内', '30天外'], top: 0, textStyle: { color: '#6b8ab5' } },
        grid: { top: 30, right: 10, bottom: 20, left: 30, containLabel: true },
        xAxis: { type: 'category', data: ['PVC', '盐酸', '盐酸', '水泥'], axisLabel: { color: '#6b8ab5' }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5' } },
        series: [
          { name: '30天内', type: 'bar', stack: 'total', data: [8, 15, 12, 14], itemStyle: { color: '#60a5fa', borderRadius: [0,0,4,4] }, barWidth: '40%' },
          { name: '30天外', type: 'bar', stack: 'total', data: [4, 10, 13, 11], itemStyle: { color: '#a78bfa', borderRadius: [4,4,0,0] }, barWidth: '40%' }
        ]
      })
    },
    initMapChart() {
      const chart = echarts.init(this.$refs.mapChart)
      const cityData = [
        { name: '北京', value: [116.4, 39.9, 320] },
        { name: '上海', value: [121.4, 31.2, 280] },
        { name: '广州', value: [113.2, 23.1, 210] },
        { name: '成都', value: [104.0, 30.6, 180] },
        { name: '西安', value: [108.9, 34.3, 150] },
        { name: '武汉', value: [114.3, 30.6, 120] },
        { name: '沈阳', value: [123.4, 41.8, 90] }
      ]
      chart.setOption({
        tooltip: { trigger: 'item', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' }, formatter: p => p.data ? `${p.data.name}: ${p.data.value[2]}吨` : '' },
        grid: { top: 10, right: 10, bottom: 10, left: 10 },
        xAxis: { show: false, min: 100, max: 130 },
        yAxis: { show: false, min: 18, max: 45 },
        series: [{
          type: 'scatter',
          data: cityData,
          symbolSize: v => Math.max(12, v[2] / 15),
          itemStyle: { color: '#00d4ff', shadowBlur: 12, shadowColor: '#00d4ff' },
          label: { show: true, formatter: p => p.data.name, position: 'top', color: '#e2e8f0', fontSize: 10 }
        }]
      })
    },
    initSalesChart() {
      const chart = echarts.init(this.$refs.salesChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        legend: { data: ['日订单量', '日销售量', '日发货量', '日完成率'], top: 0, textStyle: { color: '#6b8ab5' } },
        grid: { top: 35, right: 10, bottom: 20, left: 30, containLabel: true },
        xAxis: { type: 'category', data: ['PVC', '烧碱', '盐酸', '水泥'], axisLabel: { color: '#6b8ab5' }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: [
          { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5' } },
          { type: 'value', max: 100, axisLabel: { color: '#6b8ab5', formatter: '{value}%' }, splitLine: { show: false } }
        ],
        series: [
          { name: '日订单量', type: 'bar', data: [16, 15, 10, 19], itemStyle: { color: '#fbbf24', borderRadius: [4,4,0,0] }, barWidth: '20%' },
          { name: '日销售量', type: 'bar', data: [14, 11, 10, 18], itemStyle: { color: '#00d4ff', borderRadius: [4,4,0,0] }, barWidth: '20%' },
          { name: '日发货量', type: 'bar', data: [10, 7, 9, 15], itemStyle: { color: '#34d399', borderRadius: [4,4,0,0] }, barWidth: '20%' },
          { name: '日完成率', type: 'line', yAxisIndex: 1, data: [82, 78, 80, 86], lineStyle: { color: '#f472b6' }, itemStyle: { color: '#f472b6' } }
        ]
      })
    },
    initRings() {
      this.rings.forEach((r, i) => {
        const el = document.getElementById('ring-' + i)
        if (!el) return
        const chart = echarts.init(el)
        chart.setOption({
          color: ['#fbbf24', 'rgba(255,255,255,0.08)'],
          series: [{
            type: 'pie', radius: ['70%', '85%'], center: ['50%', '50%'], avoidLabelOverlap: false,
            label: { show: true, position: 'center', formatter: r.in + '%', fontSize: 16, fontWeight: 'bold', color: '#fbbf24' },
            data: [{ value: r.in, name: '30天内' }, { value: r.out, name: '30天外' }]
          }]
        })
      })
    },
    initLineChart(ref, color) {
      if (!ref) return
      const chart = echarts.init(ref)
      const dates = ['04-29','05-05','05-11','05-17','05-23','05-28','06-03']
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        grid: { top: 10, right: 10, bottom: 20, left: 25, containLabel: true },
        xAxis: { type: 'category', data: dates, axisLabel: { color: '#6b8ab5', fontSize: 10 }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5', fontSize: 10 } },
        series: [{ type: 'line', smooth: true, data: dates.map(() => Math.floor(Math.random() * 10 + 12)), lineStyle: { color: color, width: 2 }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color: color + '33'},{offset:1,color: color + '00'}] } }, itemStyle: { color: color } }]
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.chemical-screen { height: 100%; }
.row-main { display: flex; gap: 14px; height: 100%; }
.left-col, .right-col { width: 26%; display: flex; flex-direction: column; gap: 14px; }
.center-col { flex: 1; display: flex; flex-direction: column; gap: 14px; min-width: 0; }

.data-table { width: 100%; font-size: 12px; color: #e2e8f0; border-collapse: collapse; }
.data-table th { text-align: left; color: #6b8ab5; padding: 6px; border-bottom: 1px solid rgba(0,212,255,0.1); }
.data-table td { padding: 8px 6px; border-bottom: 1px solid rgba(255,255,255,0.03); }
.progress-bar { display: inline-block; width: 60px; height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; margin-right: 6px; vertical-align: middle; }
.progress-bar span { display: block; height: 100%; border-radius: 2px; background: linear-gradient(90deg, #00d4ff, #0ea5e9); }

.rate-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }
.rate-card { background: rgba(255,255,255,0.03); border-radius: 6px; padding: 8px; text-align: center; }
.rate-value { font-size: 18px; font-weight: 700; }
.rate-name { font-size: 11px; color: #6b8ab5; margin-top: 2px; }

.map-panel { flex: 1.5; position: relative; }
.map-stats { display: flex; justify-content: center; gap: 40px; margin-bottom: 10px; }
.map-stat { text-align: center; }
.map-stat span { display: block; font-size: 11px; color: #6b8ab5; }
.map-stat strong { font-size: 22px; font-weight: 800; }
.map-box { height: calc(100% - 60px); }
.map-legend { position: absolute; bottom: 15px; left: 50%; transform: translateX(-50%); display: flex; gap: 16px; font-size: 11px; color: #6b8ab5; }
.dot { width: 10px; height: 10px; border-radius: 2px; display: inline-block; margin-right: 4px; }
.dot.low { background: #0ea5e9; }
.dot.mid { background: #60a5fa; }
.dot.high { background: #00d4ff; }

.account-cards { display: flex; flex-direction: column; gap: 8px; margin-bottom: 10px; }
.account-card { background: rgba(255,255,255,0.03); border-radius: 8px; padding: 10px; }
.account-title { font-size: 13px; color: #e2e8f0; font-weight: 600; margin-bottom: 6px; }
.account-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; }
.account-grid span { color: #6b8ab5; display: block; }
.account-grid strong { color: #e2e8f0; font-size: 14px; }

.ring-row { display: flex; justify-content: space-around; }
.ring-box { text-align: center; }
.mini-ring { width: 90px; height: 90px; }
.ring-label { font-size: 11px; color: #6b8ab5; margin-top: -10px; }

.chart-box { width: 100%; height: 100%; }
</style>
