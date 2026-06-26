<template>
  <screen-wrapper title="销售业绩分析看板">
    <div class="sales-rank-screen">
      <div class="row row-top">
        <screen-panel title="业务员销售贡献TOP10" class="rank-panel">
          <div ref="rankChart" class="chart-box"></div>
        </screen-panel>

        <screen-panel title="销售员当日销售完成情况" class="medal-panel">
          <div class="top-three">
            <div class="medal-card second">
              <div class="crown silver"><i class="el-icon-trophy"></i></div>
              <div class="medal-name">薛凯</div>
              <div class="medal-info"><span>销量 754</span><span>目标完 84%</span></div>
            </div>
            <div class="medal-card first">
              <div class="crown gold"><i class="el-icon-trophy"></i></div>
              <div class="medal-name">冯佳</div>
              <div class="medal-info"><span>销量 1018</span><span>目标完 96%</span></div>
            </div>
            <div class="medal-card third">
              <div class="crown bronze"><i class="el-icon-trophy"></i></div>
              <div class="medal-name">王超</div>
              <div class="medal-info"><span>销量 511</span><span>目标完 79%</span></div>
            </div>
          </div>
          <div class="other-ranks">
            <div class="rank-mini" v-for="(p, i) in otherPeople" :key="i">
              <span class="mini-idx">{{ i + 4 }}</span>
              <span class="mini-name">{{ p.name }}</span>
              <span class="mini-sales">销量 {{ p.sales }}</span>
              <span class="mini-rate" :style="{color: p.rate >= 70 ? '#34d399' : '#fbbf24'}">目标完 {{ p.rate }}%</span>
            </div>
          </div>
        </screen-panel>

        <screen-panel title="大区销售情况" class="region-panel">
          <table class="region-table">
            <thead><tr><th>渠道</th><th>下单量</th><th>审单量</th><th>下单金额</th><th>审单金额</th></tr></thead>
            <tbody>
              <tr v-for="(r, i) in regionData" :key="i">
                <td>{{ r.name }}</td><td>{{ r.order }}</td><td>{{ r.check }}</td><td>{{ r.orderMoney }}</td><td>{{ r.checkMoney }}</td>
              </tr>
            </tbody>
          </table>
        </screen-panel>
      </div>

      <div class="row row-bottom">
        <screen-panel title="人均销售趋势" class="trend-panel">
          <div ref="trendChart" class="chart-box"></div>
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
      topPeople: [
        { name: '冯佳', sales: 1018, rate: 96 },
        { name: '薛凯', sales: 754, rate: 84 },
        { name: '王超', sales: 511, rate: 79 },
        { name: '吴宇', sales: 516, rate: 72 },
        { name: '何梅', sales: 270, rate: 63 },
        { name: '赵欢', sales: 249, rate: 57 },
        { name: '孙伟', sales: 235, rate: 56 },
        { name: '李萌', sales: 258, rate: 52 },
        { name: '周安', sales: 221, rate: 51 },
        { name: '郑平', sales: 198, rate: 48 }
      ],
      otherPeople: [
        { name: '吴宇', sales: 516, rate: 72 },
        { name: '何梅', sales: 270, rate: 63 },
        { name: '赵欢', sales: 249, rate: 57 },
        { name: '孙伟', sales: 235, rate: 56 },
        { name: '李萌', sales: 258, rate: 52 },
        { name: '周安', sales: 221, rate: 51 }
      ],
      regionData: [
        { name: '北京大区', order: 2190, check: 1987, orderMoney: 1488, checkMoney: 1322 },
        { name: '上海大区', order: 2010, check: 1652, orderMoney: 992, checkMoney: 870 },
        { name: '浙闽大区', order: 1030, check: 998, orderMoney: 862, checkMoney: 774 },
        { name: '苏皖大区', order: 980, check: 654, orderMoney: 1212, checkMoney: 1003 },
        { name: '华南大区', order: 1314, check: 1210, orderMoney: 960, checkMoney: 699 },
        { name: '华北大区', order: 560, check: 480, orderMoney: 568, checkMoney: 480 },
        { name: '华中大区', order: 1062, check: 870, orderMoney: 1056, checkMoney: 980 },
        { name: '东北大区', order: 856, check: 776, orderMoney: 851, checkMoney: 665 },
        { name: '西南大区', order: 778, check: 625, orderMoney: 990, checkMoney: 712 }
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initRankChart()
      this.initTrendChart()
    })
  },
  methods: {
    initRankChart() {
      const chart = echarts.init(this.$refs.rankChart)
      const data = [...this.topPeople].reverse()
      chart.setOption({
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        grid: { top: 10, right: 20, bottom: 10, left: 10, containLabel: true },
        xAxis: { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5' } },
        yAxis: { type: 'category', data: data.map(d => d.name), axisLabel: { color: '#e2e8f0' }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        series: [{
          type: 'bar', data: data.map(d => d.sales),
          barWidth: '55%',
          itemStyle: { color: new echarts.graphic.LinearGradient(1,0,0,0,[{offset:0,color:'#00d4ff'},{offset:1,color:'#0ea5e9'}]), borderRadius: [0,5,5,0] },
          label: { show: true, position: 'right', color: '#e2e8f0', fontSize: 11 }
        }]
      })
    },
    initTrendChart() {
      const chart = echarts.init(this.$refs.trendChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        legend: { data: ['当月', '同期'], top: 10, textStyle: { color: '#6b8ab5' } },
        grid: { top: 50, right: 30, bottom: 30, left: 50, containLabel: true },
        xAxis: { type: 'category', data: ['01','02','03','04','05','06','07','08','09','10','11','12'], axisLabel: { color: '#6b8ab5' }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5' } },
        series: [
          { name: '当月', type: 'line', smooth: true, data: [980, 820, 760, 440, 400, 278, 342, 396, 372, 393, 367, 384], lineStyle: { color: '#fbbf24', width: 3 }, itemStyle: { color: '#fbbf24' }, symbolSize: 5 },
          { name: '同期', type: 'line', smooth: true, data: [850, 720, 760, 234, 188, 278, 342, 396, 372, 393, 354, 274], lineStyle: { color: '#00d4ff', width: 3 }, itemStyle: { color: '#00d4ff' }, symbolSize: 5 }
        ]
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.sales-rank-screen { display: flex; flex-direction: column; gap: 14px; height: 100%; }
.row { display: flex; gap: 14px; }
.row-top { flex: 1.2; min-height: 0; }
.row-bottom { flex: 1; min-height: 0; }

.rank-panel { flex: 1; min-width: 0; }
.medal-panel { flex: 1.2; min-width: 0; }
.region-panel { flex: 1; min-width: 0; }

.top-three { display: flex; justify-content: center; align-items: flex-end; gap: 20px; margin-bottom: 16px; padding: 10px 0; }
.medal-card { width: 120px; text-align: center; background: rgba(255,255,255,0.03); border-radius: 12px; padding: 14px 10px; position: relative; }
.medal-card.first { transform: scale(1.08); background: rgba(251,191,36,0.08); border: 1px solid rgba(251,191,36,0.2); }
.medal-card.second { border: 1px solid rgba(148,163,184,0.2); }
.medal-card.third { border: 1px solid rgba(217,119,6,0.2); }
.crown { font-size: 24px; margin-bottom: 6px; }
.crown.gold { color: #fbbf24; }
.crown.silver { color: #94a3b8; }
.crown.bronze { color: #d97706; }
.medal-name { font-size: 15px; font-weight: 700; color: #e2e8f0; }
.medal-info { display: flex; flex-direction: column; gap: 2px; margin-top: 6px; font-size: 11px; color: #6b8ab5; }

.other-ranks { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
.rank-mini { display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.03); border-radius: 6px; padding: 8px; font-size: 11px; }
.mini-idx { width: 16px; height: 16px; line-height: 16px; text-align: center; background: rgba(0,212,255,0.15); color: #00d4ff; border-radius: 50%; font-size: 10px; }
.mini-name { color: #e2e8f0; width: 36px; }
.mini-sales, .mini-rate { color: #6b8ab5; }

.region-table { width: 100%; font-size: 11px; color: #e2e8f0; border-collapse: collapse; }
.region-table th { color: #6b8ab5; padding: 6px; text-align: center; border-bottom: 1px solid rgba(0,212,255,0.1); }
.region-table td { padding: 7px 4px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.03); }
.region-table tr:nth-child(even) { background: rgba(255,255,255,0.02); }

.trend-panel { width: 100%; }
.chart-box { width: 100%; height: 100%; }
</style>
