<template>
  <div class='big-screen' ref='screenRef'>
    <header class='screen-header'>
      <div class='header-left'>
        <h1 class='title'>鲸跃会展轮播大屏</h1>
        <el-button class='switch-btn' size='mini' round>轮播切换大屏</el-button>
      </div>
      <div class='header-tabs'>
        <div v-for='tab in tabs' :key='tab' :class='['tab-item', { active: activeTab === tab }]'' @click='activeTab = tab'>
          <i :class='tabIcon[tab]'></i> {{ tab }}
        </div>
      </div>
      <div class='header-right'>
        <span class='time'>{{ currentTime }}</span>
        <span class='fullscreen' @click='toggleFull'><i class='el-icon-full-screen'></i> 全屏模式</span>
      </div>
    </header>

    <main class='screen-main'>
      <section class='top-section'>
        <div class='panel sales-overview'>
          <div class='panel-title'><span>销售总览</span><i class='el-icon-warning-outline'></i></div>
          <div class='overview-cards'>
            <div class='ov-card' v-for='(c, i) in overview' :key='i'>
              <div class='ov-icon' :style='{background: c.bg}'><i :class='c.icon'></i></div>
              <div class='ov-info'>
                <div class='ov-label'>{{ c.label }}</div>
                <div class='ov-value'>{{ c.value }}</div>
                <div class='ov-change' :class='c.change.startsWith("+") ? "up" : "down"'>较昨日 {{ c.change }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class='panel top5-panel'>
          <div class='panel-title'><span>销售额 TOP5 展会</span><span class='more'>更多</span></div>
          <div class='top5-table'>
            <div class='th'><span>展会名称</span><span>销售额（元）</span><span>占比</span></div>
            <div class='tr' v-for='(row, idx) in topExhibitions' :key='idx'>
              <span><i :class='['rank', 'rank' + (idx+1)]'>{{ idx + 1 }}</i>{{ row.name }}</span>
              <span>{{ row.value }}万</span>
              <span><div class='ratio-bar'><div :style='{width: row.ratio + "%"}'></div></div>{{ row.ratio }}%</span>
            </div>
          </div>
        </div>
      </section>

      <section class='middle-section'>
        <div class='panel trend-panel'>
          <div class='panel-title'><span>销售额趋势</span>
            <div class='legend'><span class='dot blue'></span>销售额（元）<span class='dot dashed'></span>较昨日（元）</div>
          </div>
          <div ref='trendChart' class='chart-box'></div>
        </div>
        <div class='panel channel-panel'>
          <div class='panel-title'>销售额渠道占比</div>
          <div class='channel-wrap'>
            <div ref='channelChart' class='chart-box donut'></div>
            <div class='channel-list'>
              <div class='channel-item' v-for='(c, i) in channelData' :key='i'>
                <i class='dot' :style='{background: channelColors[i]}'></i>
                <span class='name'>{{ c.name }}</span>
                <span class='value'>{{ c.value }}万</span>
                <span class='ratio'>{{ c.ratio }}%</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class='key-metrics'>
        <div class='metric-card' v-for='(m, i) in keyMetrics' :key='i'>
          <div class='metric-icon'><i :class='m.icon'></i></div>
          <div class='metric-body'>
            <div class='metric-label'>{{ m.label }}</div>
            <div class='metric-value'>{{ m.value }}</div>
            <div class='metric-change' :class='m.change.startsWith("+") ? "up" : "down"'>较昨日 {{ m.change }}</div>
            <div class='sparkline'>
              <svg viewBox='0 0 120 30' preserveAspectRatio='none'>
                <polyline :points='sparkPoints(m.spark)' fill='none' :stroke='m.change.startsWith("+") ? "#67C23A" : "#F56C6C"' stroke-width='2' />
              </svg>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class='screen-footer'>
      <div class='ctrl-left'>
        <span class='ctrl-label'>轮播控制</span>
        <span class='play-state'><i class='el-icon-video-pause'></i> 自动播放中</span>
      </div>
      <div class='ctrl-center'>
        <span>当前页面</span>
        <span class='page-num'>1 / 5</span>
        <i class='el-icon-arrow-left arrow'></i>
        <i class='el-icon-video-pause pause'></i>
        <i class='el-icon-arrow-right arrow'></i>
      </div>
      <div class='ctrl-right'>
        <span>播放间隔</span>
        <span>切换效果</span>
      </div>
    </footer>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getStats } from '@/api/dashboard'
export default {
  data() {
    return {
      activeTab: '销售',
      tabs: ['销售','用户','商品','订单','财务'],
      tabIcon: { '销售': 'el-icon-shopping-cart-full', '用户': 'el-icon-user', '商品': 'el-icon-goods', '订单': 'el-icon-s-order', '财务': 'el-icon-s-finance' },
      currentTime: '',
      timer: null,
      stats: {},
      channelColors: ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399']
    }
  },
  computed: {
    overview() {
      return [
        { label: '销售额（元）', value: this.stats.totalAmount || '8,756.32万', change: '+8.6%', icon: 'el-icon-money', bg: 'linear-gradient(135deg,#409EFF,#36D1DC)' },
        { label: '订单量（笔）', value: this.stats.totalOrders || '23,856', change: '+6.3%', icon: 'el-icon-s-order', bg: 'linear-gradient(135deg,#67C23A,#95D475)' },
        { label: '客单价（元）', value: this.stats.avgPrice || '987.12', change: '+5.6%', icon: 'el-icon-user', bg: 'linear-gradient(135deg,#E6A23C,#F3D19E)' },
        { label: '转化率', value: (this.stats.convertRate || '3.62') + '%', change: '+0.42pt', icon: 'el-icon-data-line', bg: 'linear-gradient(135deg,#F56C6C,#FAB6B6)' }
      ]
    },
    topExhibitions() { return this.stats.topExhibitions || [
      { name: '智能制造博览会', value: '1,236.52', ratio: 14.1 },
      { name: '医疗健康展', value: '1,021.34', ratio: 11.7 },
      { name: '消费电子展', value: '986.71', ratio: 11.3 },
      { name: '新能源汽车展', value: '862.15', ratio: 9.8 },
      { name: '全球供应链展', value: '754.16', ratio: 8.6 }
    ]},
    channelData() { return this.stats.channelData || [
      { name: '展会现场', value: '3,245.21', ratio: 37.1 },
      { name: '线上商城', value: '2,187.64', ratio: 24.9 },
      { name: '代理分销', value: '1,536.88', ratio: 17.5 },
      { name: '企业直销', value: '1,021.43', ratio: 11.7 },
      { name: '其他渠道', value: '764.16', ratio: 8.7 }
    ]},
    keyMetrics() { return this.stats.keyMetrics || [
      { label: '新客数（人）', value: '5,678', change: '+12.5', icon: 'el-icon-user-solid', spark: [] },
      { label: '复购率', value: '27.3%', change: '+1.8pt', icon: 'el-icon-refresh', spark: [] },
      { label: '退款金额（元）', value: '186,542', change: '-5.6%', icon: 'el-icon-coin', spark: [] },
      { label: '毛利率', value: '45.7%', change: '+0.9pt', icon: 'el-icon-data-analysis', spark: [] },
      { label: '库存周转率', value: '8.2', change: '+0.3', icon: 'el-icon-box', spark: [] },
      { label: '平均发货时效（天）', value: '1.3', change: '-0.1', icon: 'el-icon-truck', spark: [] }
    ]}
  },
  async mounted() {
    this.updateTime()
    this.timer = setInterval(this.updateTime, 1000)
    this.stats = await getStats()
    this.$nextTick(() => { this.initTrendChart(); this.initChannelChart() })
    window.addEventListener('resize', this.resizeCharts)
  },
  beforeDestroy() {
    clearInterval(this.timer)
    window.removeEventListener('resize', this.resizeCharts)
  },
  methods: {
    updateTime() { this.currentTime = new Date().toLocaleString('zh-CN', { hour12: false }) },
    toggleFull() {
      const el = this.$refs.screenRef
      if (!document.fullscreenElement) el.requestFullscreen && el.requestFullscreen()
      else document.exitFullscreen && document.exitFullscreen()
    },
    sparkPoints(arr) {
      const data = (arr || []).map((v, i) => [i * 10, 30 - v / 5].join(','))
      return data.join(' ')
    },
    initTrendChart() {
      const chart = echarts.init(this.$refs.trendChart)
      const x = (this.stats.amountTrend || []).map(i => i.date)
      const y1 = (this.stats.amountTrend || []).map(i => i.value * 1000)
      const y2 = y1.map(v => v * 0.9)
      chart.setOption({
        grid: { top: 30, right: 20, bottom: 20, left: 50, containLabel: true },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: x.length ? x : ['00:00','04:00','08:00','12:00','16:00','20:00','24:00'], axisLine: { lineStyle: { color: '#4c5b70' } }, axisLabel: { color: '#8fa2b5' } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d' } }, axisLabel: { color: '#8fa2b5' } },
        series: [
          { name: '销售额', type: 'line', smooth: true, data: y1.length ? y1 : [120,220,380,520,680,850,920], lineStyle: { color: '#409EFF', width: 3 }, areaStyle: { color: { type: 'linear', x:0,y:0,x2:0,y2:1, colorStops:[{offset:0,color:'rgba(64,158,255,0.5)'},{offset:1,color:'rgba(64,158,255,0)'}] } }, itemStyle: { color: '#409EFF' } },
          { name: '较昨日', type: 'line', smooth: true, data: y2.length ? y2 : [110,200,340,480,600,720,800], lineStyle: { color: '#67C23A', width: 2, type: 'dashed' }, itemStyle: { color: '#67C23A' } }
        ]
      })
      this.trendChart = chart
    },
    initChannelChart() {
      const chart = echarts.init(this.$refs.channelChart)
      const data = this.channelData.map((c, i) => ({ name: c.name, value: c.ratio, itemStyle: { color: this.channelColors[i] } }))
      chart.setOption({
        tooltip: { trigger: 'item' },
        series: [{ type: 'pie', radius: ['55%', '75%'], center: ['50%', '50%'], label: { show: false }, data: data.length ? data : [{value:37},{value:25},{value:18},{value:12},{value:8}] }]
      })
      this.channelChart = chart
    },
    resizeCharts() { this.trendChart && this.trendChart.resize(); this.channelChart && this.channelChart.resize() }
  }
}
</script>

<style scoped>
.big-screen { width: 100vw; height: 100vh; background: #020617; color: #fff; overflow: hidden; display: flex; flex-direction: column; font-family: 'Microsoft YaHei', sans-serif; }
.screen-header { height: 70px; background: linear-gradient(90deg, rgba(8,26,56,0.95), rgba(13,42,90,0.95), rgba(8,26,56,0.95)); display: flex; align-items: center; justify-content: space-between; padding: 0 30px; border-bottom: 2px solid #1e3a5f; position: relative; }
.title { font-size: 26px; font-weight: bold; margin: 0; background: linear-gradient(90deg, #fff, #409EFF); -webkit-background-clip: text; color: transparent; text-shadow: 0 0 20px rgba(64,158,255,0.5); }
.header-left { display: flex; align-items: center; gap: 15px; }
.switch-btn { background: rgba(64,158,255,0.2); border-color: #409EFF; color: #409EFF; }
.header-tabs { position: absolute; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; }
.tab-item { padding: 8px 24px; border-radius: 4px; cursor: pointer; color: #8fa2b5; background: rgba(255,255,255,0.05); transition: all .3s; }
.tab-item.active { background: linear-gradient(180deg, rgba(64,158,255,0.3), rgba(64,158,255,0.1)); color: #fff; border-bottom: 2px solid #409EFF; box-shadow: 0 0 15px rgba(64,158,255,0.4); }
.header-right { display: flex; align-items: center; gap: 20px; color: #8fa2b5; }
.time { font-size: 16px; }
.fullscreen { cursor: pointer; color: #409EFF; }
.screen-main { flex: 1; padding: 20px; display: flex; flex-direction: column; gap: 20px; }
.panel { background: rgba(10,28,56,0.6); border: 1px solid #1e3a5f; border-radius: 8px; padding: 15px; box-shadow: 0 0 20px rgba(64,158,255,0.08); position: relative; }
.panel::before, .panel::after { content: ''; position: absolute; width: 12px; height: 12px; border: 2px solid #409EFF; }
.panel::before { top: -1px; left: -1px; border-right: none; border-bottom: none; border-top-left-radius: 8px; }
.panel::after { bottom: -1px; right: -1px; border-left: none; border-top: none; border-bottom-right-radius: 8px; }
.panel-title { display: flex; align-items: center; justify-content: space-between; color: #fff; font-size: 16px; font-weight: bold; margin-bottom: 15px; }
.more { color: #409EFF; font-size: 13px; cursor: pointer; }
.top-section { display: flex; gap: 20px; height: 170px; }
.sales-overview { flex: 2; }
.overview-cards { display: flex; gap: 15px; }
.ov-card { flex: 1; background: rgba(255,255,255,0.03); border-radius: 6px; padding: 12px; display: flex; align-items: center; gap: 12px; }
.ov-icon { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 22px; color: #fff; }
.ov-label { color: #8fa2b5; font-size: 13px; }
.ov-value { font-size: 24px; font-weight: bold; margin: 4px 0; }
.ov-change { font-size: 12px; }
.ov-change.up { color: #67C23A; }
.ov-change.down { color: #F56C6C; }
.top5-panel { flex: 1; }
.top5-table { font-size: 13px; }
.top5-table .th { display: flex; color: #8fa2b5; padding: 6px 0; border-bottom: 1px solid #1e3a5f; }
.top5-table .th span, .top5-table .tr span { flex: 1; text-align: center; }
.top5-table .tr { display: flex; padding: 9px 0; border-bottom: 1px solid rgba(30,58,95,0.4); align-items: center; }
.rank { display: inline-block; width: 18px; height: 18px; line-height: 18px; text-align: center; border-radius: 4px; font-size: 12px; margin-right: 8px; font-style: normal; background: #1e3a5f; }
.rank1 { background: #F7BA2A; color: #000; }
.rank2 { background: #C0C4CC; color: #000; }
.rank3 { background: #E6A23C; color: #000; }
.ratio-bar { width: 60px; height: 4px; background: #1e3a5f; border-radius: 2px; display: inline-block; margin-right: 8px; vertical-align: middle; }
.ratio-bar div { height: 100%; background: #409EFF; border-radius: 2px; }
.middle-section { display: flex; gap: 20px; flex: 1; min-height: 0; }
.trend-panel { flex: 1.3; }
.channel-panel { flex: 1; }
.legend { font-size: 12px; color: #8fa2b5; font-weight: normal; display: flex; align-items: center; gap: 15px; }
.legend .dot { width: 10px; height: 3px; display: inline-block; margin-right: 4px; }
.legend .dot.blue { background: #409EFF; }
.legend .dot.dashed { background: repeating-linear-gradient(90deg, #67C23A, #67C23A 4px, transparent 4px, transparent 6px); height: 2px; width: 14px; }
.chart-box { width: 100%; height: 100%; }
.donut { height: 220px; }
.channel-wrap { display: flex; height: calc(100% - 40px); }
.channel-list { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 12px; padding-left: 10px; }
.channel-item { display: flex; align-items: center; font-size: 13px; }
.channel-item .dot { width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }
.channel-item .name { flex: 1; color: #8fa2b5; }
.channel-item .value { width: 80px; color: #fff; text-align: right; }
.channel-item .ratio { width: 50px; color: #409EFF; text-align: right; }
.key-metrics { display: flex; gap: 15px; height: 130px; }
.metric-card { flex: 1; background: rgba(10,28,56,0.6); border-radius: 8px; border: 1px solid #1e3a5f; padding: 12px; display: flex; gap: 10px; }
.metric-icon { width: 36px; height: 36px; background: rgba(64,158,255,0.15); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #409EFF; font-size: 18px; }
.metric-body { flex: 1; }
.metric-label { color: #8fa2b5; font-size: 12px; }
.metric-value { font-size: 20px; font-weight: bold; margin: 4px 0; }
.metric-change { font-size: 11px; }
.metric-change.up { color: #67C23A; }
.metric-change.down { color: #F56C6C; }
.sparkline { height: 24px; margin-top: 4px; }
.sparkline svg { width: 100%; height: 100%; }
.screen-footer { height: 50px; background: rgba(10,28,56,0.8); border-top: 1px solid #1e3a5f; display: flex; align-items: center; justify-content: space-between; padding: 0 30px; color: #8fa2b5; font-size: 13px; }
.ctrl-left, .ctrl-right { display: flex; gap: 20px; align-items: center; }
.ctrl-label { color: #fff; }
.play-state { color: #409EFF; }
.ctrl-center { display: flex; align-items: center; gap: 15px; }
.page-num { color: #fff; font-weight: bold; font-size: 16px; }
.arrow { font-size: 18px; cursor: pointer; color: #fff; }
.pause { font-size: 28px; cursor: pointer; color: #409EFF; }
</style>
