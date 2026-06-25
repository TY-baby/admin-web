<template>
  <div class="big-screen" ref="screenRef">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-grid"></div>
      <div class="bg-glow bg-glow-1"></div>
      <div class="bg-glow bg-glow-2"></div>
    </div>

    <header class="screen-header">
      <div class="header-deco-left"></div>
      <div class="header-deco-right"></div>
      <div class="header-left">
        <h1 class="title">鲸跃会展轮播大屏</h1>
        <el-button class="switch-btn" size="mini" round>轮播切换</el-button>
      </div>
      <div class="header-tabs">
        <div v-for="tab in tabs" :key="tab"
             :class="['tab-item', { active: activeTab === tab }]"
             @click="switchTab(tab)">
          <i :class="tabIcon[tab]"></i> {{ tab }}
        </div>
      </div>
      <div class="header-right">
        <span class="time"><i class="el-icon-time"></i> {{ currentTime }}</span>
        <span class="fullscreen" @click="toggleFull"><i class="el-icon-full-screen"></i> 全屏</span>
      </div>
    </header>

    <main class="screen-main">
      <transition name="fade-slide" mode="out-in">
        <!-- 销售 Tab -->
        <div v-if="activeTab === '销售'" key="sales" class="tab-content">
          <section class="top-section">
            <div class="panel sales-overview">
              <div class="panel-title"><span>销售总览</span><i class="el-icon-warning-outline title-icon"></i></div>
              <div class="overview-cards">
                <div class="ov-card" v-for="(c, i) in overview" :key="i">
                  <div class="ov-icon" :style="{background: c.bg}"><i :class="c.icon"></i></div>
                  <div class="ov-info">
                    <div class="ov-label">{{ c.label }}</div>
                    <div class="ov-value">{{ c.value }}</div>
                    <div class="ov-change" :class="c.change.startsWith('+') ? 'up' : 'down'">
                      <i :class="c.change.startsWith('+') ? 'el-icon-top' : 'el-icon-bottom'"></i> {{ c.change }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="panel top5-panel">
              <div class="panel-title"><span>销售额 TOP5 展会</span><span class="more">更多 <i class="el-icon-arrow-right"></i></span></div>
              <div class="top5-table">
                <div class="th"><span>展会名称</span><span>销售额（元）</span><span>占比</span></div>
                <div class="tr" v-for="(row, idx) in topExhibitions" :key="idx">
                  <span><span :class="['rank', 'rank' + (idx + 1)]">{{ idx + 1 }}</span>{{ row.name }}</span>
                  <span class="amount-val">{{ row.value }}万</span>
                  <span><span class="ratio-bar"><span :style="{width: row.ratio + '%'}"></span></span>{{ row.ratio }}%</span>
                </div>
              </div>
            </div>
          </section>

          <section class="middle-section">
            <div class="panel trend-panel">
              <div class="panel-title"><span>销售额趋势</span>
                <div class="legend"><span class="dot blue"></span>销售额（元）<span class="dot dashed"></span>较昨日（元）</div>
              </div>
              <div ref="trendChart" class="chart-box"></div>
            </div>
            <div class="panel channel-panel">
              <div class="panel-title">销售额渠道占比</div>
              <div class="channel-wrap">
                <div ref="channelChart" class="chart-box donut"></div>
                <div class="channel-list">
                  <div class="channel-item" v-for="(c, i) in channelData" :key="i">
                    <i class="dot" :style="{background: channelColors[i]}"></i>
                    <span class="name">{{ c.name }}</span>
                    <span class="value">{{ c.value }}万</span>
                    <span class="ratio">{{ c.ratio }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section class="key-metrics">
            <div class="metric-card" v-for="(m, i) in keyMetrics" :key="i">
              <div class="metric-icon"><i :class="m.icon"></i></div>
              <div class="metric-body">
                <div class="metric-label">{{ m.label }}</div>
                <div class="metric-value">{{ m.value }}</div>
                <div class="metric-change" :class="String(m.change).startsWith('+') ? 'up' : 'down'">
                  <i :class="String(m.change).startsWith('+') ? 'el-icon-top' : 'el-icon-bottom'" style="font-size:10px"></i> {{ m.change }}
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- 用户 Tab -->
        <div v-else-if="activeTab === '用户'" key="users" class="tab-content">
          <section class="top-section">
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>用户增长趋势</span></div>
              <div ref="userTrendChart" class="chart-box" style="height:200px"></div>
            </div>
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>用户来源分布</span></div>
              <div ref="userSourceChart" class="chart-box" style="height:200px"></div>
            </div>
          </section>
          <section class="middle-section">
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>活跃用户排行</span></div>
              <div ref="userRankChart" class="chart-box"></div>
            </div>
          </section>
        </div>

        <!-- 商品 Tab -->
        <div v-else-if="activeTab === '商品'" key="products" class="tab-content">
          <section class="top-section">
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>商品销量排行</span></div>
              <div ref="productRankChart" class="chart-box" style="height:200px"></div>
            </div>
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>商品分类占比</span></div>
              <div ref="productCatChart" class="chart-box" style="height:200px"></div>
            </div>
          </section>
          <section class="middle-section">
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>库存周转趋势</span></div>
              <div ref="productStockChart" class="chart-box"></div>
            </div>
          </section>
        </div>

        <!-- 订单 Tab -->
        <div v-else-if="activeTab === '订单'" key="orders" class="tab-content">
          <section class="top-section">
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>订单量趋势</span></div>
              <div ref="orderTrendChart" class="chart-box" style="height:200px"></div>
            </div>
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>订单状态分布</span></div>
              <div ref="orderStatusChart" class="chart-box" style="height:200px"></div>
            </div>
          </section>
          <section class="middle-section">
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>近7天订单金额</span></div>
              <div ref="orderAmountChart" class="chart-box"></div>
            </div>
          </section>
        </div>

        <!-- 财务 Tab -->
        <div v-else-if="activeTab === '财务'" key="finance" class="tab-content">
          <section class="top-section">
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>收入趋势</span></div>
              <div ref="incomeTrendChart" class="chart-box" style="height:200px"></div>
            </div>
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>支出构成</span></div>
              <div ref="expenseChart" class="chart-box" style="height:200px"></div>
            </div>
          </section>
          <section class="middle-section">
            <div class="panel" style="flex:1">
              <div class="panel-title"><span>利润走势</span></div>
              <div ref="profitChart" class="chart-box"></div>
            </div>
          </section>
        </div>
      </transition>
    </main>

    <footer class="screen-footer">
      <div class="ctrl-left">
        <span class="play-state" @click="autoPlay = !autoPlay">
          <i :class="autoPlay ? 'el-icon-video-pause' : 'el-icon-video-play'"></i>
          {{ autoPlay ? '自动播放中' : '已暂停' }}
        </span>
      </div>
      <div class="ctrl-center">
        <i class="el-icon-arrow-left arrow" @click="prevTab"></i>
        <div class="page-dots">
          <span v-for="(tab, idx) in tabs" :key="idx" :class="['dot', { active: activeTab === tab }]" @click="switchTab(tab)"></span>
        </div>
        <i class="el-icon-arrow-right arrow" @click="nextTab"></i>
      </div>
      <div class="ctrl-right">
        <span>间隔 {{ autoPlayInterval }}s</span>
        <span>{{ activeTab }} {{ currentPage }}/{{ totalPages }}</span>
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
      tabIcon: {
        '销售': 'el-icon-shopping-cart-full',
        '用户': 'el-icon-user',
        '商品': 'el-icon-goods',
        '订单': 'el-icon-s-order',
        '财务': 'el-icon-s-finance'
      },
      currentTime: '',
      timer: null,
      autoPlayTimer: null,
      autoPlay: true,
      autoPlayInterval: 15,
      stats: {},
      channelColors: ['#00d4ff', '#a78bfa', '#fbbf24', '#34d399', '#f472b6'],
      charts: []
    }
  },
  computed: {
    currentPage() { return this.tabs.indexOf(this.activeTab) + 1 },
    totalPages() { return this.tabs.length },
    overview() {
      const s = this.stats
      return [
        { label: '销售额（元）', value: s.totalAmount ? s.totalAmount + '万' : '8,756.32万', change: '+8.6%', icon: 'el-icon-money', bg: 'linear-gradient(135deg,#0ea5e9,#00d4ff)' },
        { label: '订单量（笔）', value: s.totalOrders || '23,856', change: '+6.3%', icon: 'el-icon-s-order', bg: 'linear-gradient(135deg,#8b5cf6,#a78bfa)' },
        { label: '客单价（元）', value: s.avgPrice || '987.12', change: '+5.6%', icon: 'el-icon-user', bg: 'linear-gradient(135deg,#f59e0b,#fbbf24)' },
        { label: '转化率', value: (s.convertRate || '3.62') + '%', change: '+0.42pt', icon: 'el-icon-data-line', bg: 'linear-gradient(135deg,#10b981,#34d399)' }
      ]
    },
    topExhibitions() {
      return this.stats.topExhibitions || [
        { name: '智能制造博览会', value: '1,236.52', ratio: 14.1 },
        { name: '医疗健康展', value: '1,021.34', ratio: 11.7 },
        { name: '消费电子展', value: '986.71', ratio: 11.3 },
        { name: '新能源汽车展', value: '862.15', ratio: 9.8 },
        { name: '全球供应链展', value: '754.16', ratio: 8.6 }
      ]
    },
    channelData() {
      return this.stats.channelData || [
        { name: '展会现场', value: '3,245.21', ratio: 37.1 },
        { name: '线上商城', value: '2,187.64', ratio: 24.9 },
        { name: '代理分销', value: '1,536.88', ratio: 17.5 },
        { name: '企业直销', value: '1,021.43', ratio: 11.7 },
        { name: '其他渠道', value: '764.16', ratio: 8.7 }
      ]
    },
    keyMetrics() {
      return this.stats.keyMetrics || [
        { label: '新客数（人）', value: '5,678', change: '+12.5', icon: 'el-icon-user-solid', spark: [] },
        { label: '复购率', value: '27.3%', change: '+1.8pt', icon: 'el-icon-refresh', spark: [] },
        { label: '退款金额（元）', value: '186,542', change: '-5.6%', icon: 'el-icon-coin', spark: [] },
        { label: '毛利率', value: '45.7%', change: '+0.9pt', icon: 'el-icon-data-analysis', spark: [] },
        { label: '库存周转率', value: '8.2', change: '+0.3', icon: 'el-icon-box', spark: [] },
        { label: '平均发货时效（天）', value: '1.3', change: '-0.1', icon: 'el-icon-truck', spark: [] }
      ]
    }
  },
  watch: {
    activeTab() {
      clearTimeout(this._tabTimer)
      this._tabTimer = setTimeout(() => {
        this.initTabCharts()
        this.charts.forEach(c => {
          try { c.resize() } catch(e) {}
        })
      }, 500)
    }
  },
  async mounted() {
    this.updateTime()
    this.timer = setInterval(this.updateTime, 1000)
    this.startAutoPlay()
    this.$nextTick(() => this.initTabCharts())
    this.loadDataAsync()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    clearInterval(this.timer)
    clearInterval(this.autoPlayTimer)
    clearTimeout(this._tabTimer)
    window.removeEventListener('resize', this.handleResize)
    this.charts.forEach(c => { try { c && c.dispose() } catch(e) {} })
  },
  methods: {
    loadDataAsync() {
      const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 3000))
      Promise.race([getStats(), timeout]).then(data => {
        this.stats = data
        this.$nextTick(() => this.initTabCharts())
      }).catch(() => {
        console.warn('数据加载超时，使用默认数据')
      })
    },
    switchTab(tab) { this.activeTab = tab },
    prevTab() {
      const idx = this.tabs.indexOf(this.activeTab)
      this.activeTab = this.tabs[(idx - 1 + this.tabs.length) % this.tabs.length]
    },
    nextTab() {
      const idx = this.tabs.indexOf(this.activeTab)
      this.activeTab = this.tabs[(idx + 1) % this.tabs.length]
    },
    startAutoPlay() {
      this.autoPlayTimer = setInterval(() => {
        if (this.autoPlay) this.nextTab()
      }, this.autoPlayInterval * 1000)
    },
    updateTime() { this.currentTime = new Date().toLocaleString('zh-CN', { hour12: false }) },
    toggleFull() {
      const el = this.$refs.screenRef
      if (!document.fullscreenElement) el.requestFullscreen && el.requestFullscreen()
      else document.exitFullscreen && document.exitFullscreen()
    },
    handleResize() { this.charts.forEach(c => c && c.resize()) },
    makeChart(ref) {
      const el = this.$refs[ref]
      if (!el) return null
      this.charts = this.charts.filter(c => {
        if (!c || !c.getDom() || !document.contains(c.getDom())) {
          try { c.dispose() } catch(e) {}
          return false
        }
        return true
      })
      const existing = this.charts.find(c => c.getDom() === el)
      if (existing) { existing.dispose() }
      const chart = echarts.init(el)
      this.charts.push(chart)
      return chart
    },
    initTabCharts() {
      if (this.activeTab === '销售') { this.initTrendChart(); this.initChannelChart() }
      else if (this.activeTab === '用户') { this.initUserCharts() }
      else if (this.activeTab === '商品') { this.initProductCharts() }
      else if (this.activeTab === '订单') { this.initOrderCharts() }
      else if (this.activeTab === '财务') { this.initFinanceCharts() }
    },

    // ===== 图表配色主题 =====
    chartTheme() {
      return {
        axisLine: '#2a3a5e',
        axisLabel: '#6b8ab5',
        splitLine: '#1a2744',
        tooltipBg: 'rgba(8,18,46,0.95)',
        tooltipBorder: '#1e3a5f',
        colors: ['#00d4ff','#a78bfa','#fbbf24','#34d399','#f472b6','#0ea5e9','#8b5cf6']
      }
    },

    initTrendChart() {
      const chart = this.makeChart('trendChart')
      if (!chart) return
      const t = this.chartTheme()
      const x = (this.stats.amountTrend || []).map(i => i.date)
      const y1 = (this.stats.amountTrend || []).map(i => i.value * 1000)
      const y2 = y1.map(v => v * 0.9)
      chart.setOption({
        grid: { top: 30, right: 20, bottom: 30, left: 50, containLabel: true },
        tooltip: { trigger: 'axis', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0', fontSize: 12 } },
        xAxis: { type: 'category', data: x.length ? x : ['06-19','06-20','06-21','06-22','06-23','06-24','06-25'], axisLine: { lineStyle: { color: t.axisLine } }, axisLabel: { color: t.axisLabel }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: t.splitLine, type: 'dashed' } }, axisLabel: { color: t.axisLabel, formatter: v => v >= 1000 ? (v/1000) + 'k' : v }, axisLine: { show: false } },
        series: [
          { name: '销售额', type: 'line', smooth: true, data: y1.length ? y1 : [120000,220000,380000,520000,680000,850000,920000],
            lineStyle: { color: '#00d4ff', width: 3, shadowColor: 'rgba(0,212,255,0.5)', shadowBlur: 12 },
            areaStyle: { color: { type: 'linear', x:0,y:0,x2:0,y2:1, colorStops:[{offset:0,color:'rgba(0,212,255,0.25)'},{offset:1,color:'rgba(0,212,255,0)'}] } },
            itemStyle: { color: '#00d4ff' }, symbolSize: 6 },
          { name: '较昨日', type: 'line', smooth: true, data: y2.length ? y2 : [110000,200000,340000,480000,600000,720000,800000],
            lineStyle: { color: '#a78bfa', width: 2, type: 'dashed' }, itemStyle: { color: '#a78bfa' }, symbolSize: 4 }
        ],
        animationDuration: 1200, animationEasing: 'cubicOut'
      })
    },

    initChannelChart() {
      const chart = this.makeChart('channelChart')
      if (!chart) return
      const t = this.chartTheme()
      const data = this.channelData.map((c, i) => ({ name: c.name, value: c.ratio, itemStyle: { color: this.channelColors[i] } }))
      chart.setOption({
        tooltip: { trigger: 'item', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
        series: [{ type: 'pie', radius: ['50%', '72%'], center: ['50%', '50%'], label: { show: false },
          emphasis: { label: { show: true, color: '#e2e8f0', fontWeight: 'bold' }, itemStyle: { shadowBlur: 20, shadowColor: 'rgba(0,0,0,0.3)' } },
          itemStyle: { borderRadius: 6, borderColor: '#0c1a3a', borderWidth: 3 },
          data: data.length ? data : [{value:37,name:'展会现场'},{value:25,name:'线上商城'},{value:18,name:'代理分销'},{value:12,name:'企业直销'},{value:8,name:'其他'}]
        }],
        animationDuration: 1200
      })
    },

    initUserCharts() {
      const t = this.chartTheme()
      const trend = this.makeChart('userTrendChart')
      if (trend) {
        trend.setOption({
          grid: { top: 20, right: 20, bottom: 25, left: 40 },
          tooltip: { trigger: 'axis', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          xAxis: { type: 'category', data: ['周一','周二','周三','周四','周五','周六','周日'], axisLabel: { color: t.axisLabel }, axisLine: { lineStyle: { color: t.axisLine } }, axisTick: { show: false } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: t.splitLine, type: 'dashed' } }, axisLabel: { color: t.axisLabel } },
          series: [
            { name: '新增用户', type: 'bar', data: [45,62,38,71,55,89,67], itemStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'#00d4ff'},{offset:1,color:'#0ea5e9'}]), borderRadius: [6,6,0,0] }, barWidth: '40%' },
            { name: '活跃用户', type: 'line', smooth: true, data: [320,380,350,420,390,510,480], lineStyle: { color: '#a78bfa', width: 2.5 }, itemStyle: { color: '#a78bfa' }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(167,139,250,0.2)'},{offset:1,color:'rgba(167,139,250,0)'}] } } }
          ]
        })
      }
      const source = this.makeChart('userSourceChart')
      if (source) {
        source.setOption({
          tooltip: { trigger: 'item', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          color: t.colors,
          series: [{ type: 'pie', radius: '65%', roseType: 'area', label: { color: t.axisLabel, fontSize: 11 },
            itemStyle: { borderRadius: 6, borderColor: '#0c1a3a', borderWidth: 3 },
            data: [{name:'官网',value:35},{name:'推广',value:28},{name:'转介绍',value:22},{name:'展会',value:18},{name:'其他',value:12}]
          }]
        })
      }
      const rank = this.makeChart('userRankChart')
      if (rank) {
        const names = ['王明','李华','张强','刘芳','陈伟','赵丽','孙磊','周洋','吴婷','郑凯']
        const vals = [98,87,76,72,68,65,61,58,52,48]
        rank.setOption({
          grid: { top: 10, right: 80, bottom: 10, left: 10, containLabel: true },
          tooltip: { trigger: 'axis', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          xAxis: { type: 'value', splitLine: { lineStyle: { color: t.splitLine, type: 'dashed' } }, axisLabel: { color: t.axisLabel } },
          yAxis: { type: 'category', data: names.reverse(), axisLabel: { color: '#c8d8ec', fontSize: 12 }, axisLine: { show: false }, axisTick: { show: false } },
          series: [{ type: 'bar', data: vals.reverse().map((v,i) => ({value:v, itemStyle: { color: new echarts.graphic.LinearGradient(0,0,1,0,[{offset:0,color:t.colors[i%7]},{offset:1,color:t.colors[(i+1)%7]}]), borderRadius:[0,6,6,0] }})), barWidth: '50%',
            label: { show: true, position: 'right', color: '#c8d8ec', fontSize: 12 }
          }]
        })
      }
    },

    initProductCharts() {
      const t = this.chartTheme()
      const rank = this.makeChart('productRankChart')
      if (rank) {
        rank.setOption({
          grid: { top: 10, right: 20, bottom: 25, left: 40 },
          tooltip: { trigger: 'axis', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          xAxis: { type: 'category', data: ['CRM标准版','CRM高级版','数据大屏','实施服务','定制开发'], axisLabel: { color: t.axisLabel, rotate: 15 }, axisLine: { lineStyle: { color: t.axisLine } }, axisTick: { show: false } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: t.splitLine, type: 'dashed' } }, axisLabel: { color: t.axisLabel } },
          series: [{ type: 'bar', data: [156,98,72,45,32].map((v,i) => ({value:v, itemStyle:{color:t.colors[i]}})), barWidth: '45%', itemStyle: { borderRadius: [6,6,0,0] },
            label: { show: true, position: 'top', color: '#c8d8ec', fontSize: 12 }
          }]
        })
      }
      const cat = this.makeChart('productCatChart')
      if (cat) {
        cat.setOption({
          tooltip: { trigger: 'item', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          color: t.colors,
          series: [{ type: 'pie', radius: ['40%','70%'], label: { color: t.axisLabel },
            itemStyle: { borderRadius: 6, borderColor: '#0c1a3a', borderWidth: 3 },
            data: [{name:'软件',value:68},{name:'服务',value:18},{name:'硬件',value:8},{name:'培训',value:4},{name:'其他',value:2}]
          }]
        })
      }
      const stock = this.makeChart('productStockChart')
      if (stock) {
        stock.setOption({
          grid: { top: 30, right: 20, bottom: 30, left: 50 },
          tooltip: { trigger: 'axis', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          legend: { data: ['入库','出库','库存'], top: 0, textStyle: { color: t.axisLabel } },
          xAxis: { type: 'category', data: ['1月','2月','3月','4月','5月','6月'], axisLabel: { color: t.axisLabel }, axisLine: { lineStyle: { color: t.axisLine } }, axisTick: { show: false } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: t.splitLine, type: 'dashed' } }, axisLabel: { color: t.axisLabel } },
          series: [
            { name: '入库', type: 'bar', data: [120,150,90,180,130,160], itemStyle: { color: '#00d4ff', borderRadius: [4,4,0,0] }, barWidth: '25%' },
            { name: '出库', type: 'bar', data: [100,130,110,160,120,140], itemStyle: { color: '#a78bfa', borderRadius: [4,4,0,0] }, barWidth: '25%' },
            { name: '库存', type: 'line', smooth: true, data: [500,520,500,520,530,550], lineStyle: { color: '#fbbf24', width: 2.5 }, itemStyle: { color: '#fbbf24' }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(251,191,36,0.15)'},{offset:1,color:'rgba(251,191,36,0)'}] } } }
          ]
        })
      }
    },

    initOrderCharts() {
      const t = this.chartTheme()
      const trend = this.makeChart('orderTrendChart')
      if (trend) {
        trend.setOption({
          grid: { top: 20, right: 20, bottom: 25, left: 40 },
          tooltip: { trigger: 'axis', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          xAxis: { type: 'category', data: ['周一','周二','周三','周四','周五','周六','周日'], axisLabel: { color: t.axisLabel }, axisLine: { lineStyle: { color: t.axisLine } }, axisTick: { show: false } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: t.splitLine, type: 'dashed' } }, axisLabel: { color: t.axisLabel } },
          series: [
            { type: 'bar', data: [28,35,22,41,38,52,45].map((v,i) => ({value:v, itemStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'#00d4ff'},{offset:1,color:'#0ea5e9'}])}})), barWidth: '40%', itemStyle: { borderRadius: [6,6,0,0] } }
          ]
        })
      }
      const status = this.makeChart('orderStatusChart')
      if (status) {
        status.setOption({
          tooltip: { trigger: 'item', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          color: t.colors,
          series: [{ type: 'pie', radius: ['40%','70%'], label: { color: t.axisLabel, fontSize: 11 },
            itemStyle: { borderRadius: 6, borderColor: '#0c1a3a', borderWidth: 3 },
            data: [{name:'待确认',value:18},{name:'已确认',value:25},{name:'生产中',value:15},{name:'已发货',value:22},{name:'已完成',value:38},{name:'已取消',value:5}]
          }]
        })
      }
      const amount = this.makeChart('orderAmountChart')
      if (amount) {
        amount.setOption({
          grid: { top: 30, right: 20, bottom: 30, left: 50 },
          tooltip: { trigger: 'axis', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' }, formatter: p => p[0].name + '<br/>金额: ¥' + p[0].value.toLocaleString() },
          xAxis: { type: 'category', data: ['周一','周二','周三','周四','周五','周六','周日'], axisLabel: { color: t.axisLabel }, axisLine: { lineStyle: { color: t.axisLine } }, axisTick: { show: false } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: t.splitLine, type: 'dashed' } }, axisLabel: { color: t.axisLabel, formatter: v => v >= 10000 ? (v/10000) + 'w' : v } },
          series: [
            { type: 'line', smooth: true, data: [32000,45000,28000,62000,51000,78000,65000],
              lineStyle: { color: '#f472b6', width: 3, shadowColor: 'rgba(244,114,182,0.4)', shadowBlur: 12 },
              itemStyle: { color: '#f472b6', borderWidth: 3, borderColor: '#1a1040' }, symbolSize: 8,
              areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(244,114,182,0.25)'},{offset:1,color:'rgba(244,114,182,0)'}] } }
            }
          ]
        })
      }
    },

    initFinanceCharts() {
      const t = this.chartTheme()
      const income = this.makeChart('incomeTrendChart')
      if (income) {
        income.setOption({
          grid: { top: 20, right: 20, bottom: 25, left: 50 },
          tooltip: { trigger: 'axis', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          xAxis: { type: 'category', data: ['1月','2月','3月','4月','5月','6月'], axisLabel: { color: t.axisLabel }, axisLine: { lineStyle: { color: t.axisLine } }, axisTick: { show: false } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: t.splitLine, type: 'dashed' } }, axisLabel: { color: t.axisLabel, formatter: v => (v/10000) + 'w' } },
          series: [
            { type: 'bar', data: [180000,220000,195000,260000,310000,285000].map((v,i) => ({value:v, itemStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'#34d399'},{offset:1,color:'#10b981'}])}})), barWidth: '40%', itemStyle: { borderRadius: [6,6,0,0] } }
          ]
        })
      }
      const expense = this.makeChart('expenseChart')
      if (expense) {
        expense.setOption({
          tooltip: { trigger: 'item', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          color: t.colors,
          series: [{ type: 'pie', radius: '65%', label: { color: t.axisLabel },
            itemStyle: { borderRadius: 6, borderColor: '#0c1a3a', borderWidth: 3 },
            data: [{name:'人力成本',value:42},{name:'运营费用',value:25},{name:'营销推广',value:18},{name:'技术投入',value:10},{name:'其他',value:5}]
          }]
        })
      }
      const profit = this.makeChart('profitChart')
      if (profit) {
        profit.setOption({
          grid: { top: 30, right: 20, bottom: 30, left: 50 },
          tooltip: { trigger: 'axis', backgroundColor: t.tooltipBg, borderColor: t.tooltipBorder, textStyle: { color: '#e2e8f0' } },
          legend: { data: ['收入','支出','利润'], top: 0, textStyle: { color: t.axisLabel } },
          xAxis: { type: 'category', data: ['1月','2月','3月','4月','5月','6月'], axisLabel: { color: t.axisLabel }, axisLine: { lineStyle: { color: t.axisLine } }, axisTick: { show: false } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: t.splitLine, type: 'dashed' } }, axisLabel: { color: t.axisLabel, formatter: v => (v/10000) + 'w' } },
          series: [
            { name: '收入', type: 'bar', data: [180000,220000,195000,260000,310000,285000], itemStyle: { color: '#00d4ff', borderRadius: [5,5,0,0] }, barWidth: '20%' },
            { name: '支出', type: 'bar', data: [120000,140000,130000,160000,180000,170000], itemStyle: { color: '#a78bfa', borderRadius: [5,5,0,0] }, barWidth: '20%' },
            { name: '利润', type: 'line', smooth: true, data: [60000,80000,65000,100000,130000,115000], lineStyle: { color: '#34d399', width: 3 }, itemStyle: { color: '#34d399' }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(52,211,153,0.2)'},{offset:1,color:'rgba(52,211,153,0)'}] } }, symbolSize: 6 }
          ]
        })
      }
    }
  }
}
</script>

<style scoped>
/* ===== 全局 ===== */
.big-screen {
  width: 100vw; height: 100vh; overflow: hidden; display: flex; flex-direction: column;
  background: #070d24;
  color: #e2e8f0;
  font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
  position: relative;
}

/* ===== 背景装饰 ===== */
.bg-decoration { position: absolute; inset: 0; pointer-events: none; overflow: hidden; z-index: 0; }
.bg-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}
.bg-glow { position: absolute; border-radius: 50%; filter: blur(120px); opacity: 0.15; }
.bg-glow-1 { width: 600px; height: 600px; background: #0ea5e9; top: -200px; right: -100px; }
.bg-glow-2 { width: 500px; height: 500px; background: #8b5cf6; bottom: -150px; left: -100px; }

/* ===== 头部 ===== */
.screen-header {
  height: 64px; min-height: 64px; position: relative; z-index: 1;
  background: linear-gradient(180deg, rgba(7,13,36,0.98) 0%, rgba(10,20,50,0.95) 100%);
  display: flex; align-items: center; justify-content: space-between; padding: 0 24px;
  border-bottom: 1px solid rgba(0,212,255,0.15);
}
.screen-header::after {
  content: ''; position: absolute; bottom: -1px; left: 50%; transform: translateX(-50%);
  width: 40%; height: 2px;
  background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}
.header-deco-left, .header-deco-right {
  position: absolute; top: 50%; width: 80px; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,212,255,0.4));
}
.header-deco-left { left: 220px; }
.header-deco-right { right: 220px; transform: rotate(180deg); }

.title {
  font-size: 22px; font-weight: 700; margin: 0; letter-spacing: 3px;
  background: linear-gradient(135deg, #00d4ff 0%, #a78bfa 50%, #00d4ff 100%);
  background-size: 200% auto;
  -webkit-background-clip: text; color: transparent;
  animation: titleShine 4s linear infinite;
}
@keyframes titleShine { to { background-position: 200% center; } }

.header-left { display: flex; align-items: center; gap: 14px; z-index: 1; }
.switch-btn {
  background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.3);
  color: #00d4ff; font-size: 11px; padding: 5px 14px;
}
.switch-btn:hover { background: rgba(0,212,255,0.2); border-color: #00d4ff; color: #00d4ff; }

.header-tabs { position: absolute; left: 50%; transform: translateX(-50%); display: flex; gap: 4px; z-index: 1; }
.tab-item {
  padding: 7px 20px; border-radius: 6px; cursor: pointer; color: #6b8ab5;
  background: rgba(255,255,255,0.03); transition: all 0.3s ease; font-size: 13px;
  border: 1px solid transparent;
}
.tab-item:hover { background: rgba(0,212,255,0.08); color: #a0c4e8; border-color: rgba(0,212,255,0.15); }
.tab-item.active {
  background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(167,139,250,0.1));
  color: #fff; border-color: rgba(0,212,255,0.4);
  box-shadow: 0 0 20px rgba(0,212,255,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
}

.header-right { display: flex; align-items: center; gap: 18px; color: #6b8ab5; font-size: 13px; z-index: 1; }
.time { font-size: 13px; font-variant-numeric: tabular-nums; }
.fullscreen { cursor: pointer; color: #00d4ff; font-size: 13px; transition: color 0.2s; }
.fullscreen:hover { color: #5ce4ff; }

/* ===== 主体 ===== */
.screen-main { flex: 1; padding: 14px 18px; display: flex; flex-direction: column; min-height: 0; overflow: hidden; position: relative; z-index: 1; }

.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.4s ease; }
.fade-slide-enter { opacity: 0; transform: translateX(30px); }
.fade-slide-leave-to { opacity: 0; transform: translateX(-30px); }

.tab-content { display: flex; flex-direction: column; gap: 12px; height: 100%; }

/* ===== 面板 ===== */
.panel {
  background: linear-gradient(135deg, rgba(12,26,58,0.8) 0%, rgba(8,18,46,0.9) 100%);
  border: 1px solid rgba(0,212,255,0.1);
  border-radius: 10px; padding: 14px 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.03);
  position: relative; backdrop-filter: blur(10px);
}
.panel::before {
  content: ''; position: absolute; top: 0; left: 20px; right: 20px; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent);
}
.panel-title {
  display: flex; align-items: center; justify-content: space-between;
  color: #e2e8f0; font-size: 14px; font-weight: 600; margin-bottom: 12px;
}
.title-icon { color: #6b8ab5; font-weight: normal; }
.more { color: #00d4ff; font-size: 12px; cursor: pointer; font-weight: normal; display: flex; align-items: center; gap: 3px; }
.more:hover { color: #5ce4ff; }

/* ===== 销售总览卡片 ===== */
.top-section { display: flex; gap: 14px; flex-shrink: 0; }
.sales-overview { flex: 2; }
.overview-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.ov-card {
  background: rgba(255,255,255,0.02); border-radius: 8px; padding: 12px;
  display: flex; align-items: center; gap: 12px; transition: all 0.3s;
  border: 1px solid rgba(255,255,255,0.04);
}
.ov-card:hover { background: rgba(0,212,255,0.04); border-color: rgba(0,212,255,0.15); transform: translateY(-2px); }
.ov-icon { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; color: #fff; flex-shrink: 0; }
.ov-label { color: #6b8ab5; font-size: 11px; }
.ov-value { font-size: 20px; font-weight: 700; margin: 2px 0; color: #fff; font-variant-numeric: tabular-nums; }
.ov-change { font-size: 11px; display: flex; align-items: center; gap: 2px; }
.ov-change.up { color: #34d399; }
.ov-change.down { color: #f87171; }

/* ===== TOP5 表格 ===== */
.top5-panel { flex: 1; overflow: hidden; }
.top5-table { font-size: 12px; }
.top5-table .th { display: flex; color: #6b8ab5; padding: 6px 0; border-bottom: 1px solid rgba(0,212,255,0.1); font-size: 11px; }
.top5-table .th span, .top5-table .tr span { flex: 1; text-align: center; }
.top5-table .tr { display: flex; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.03); align-items: center; transition: background 0.2s; }
.top5-table .tr:hover { background: rgba(0,212,255,0.04); }
.amount-val { color: #fbbf24; font-weight: 600; }
.rank { display: inline-block; width: 18px; height: 18px; line-height: 18px; text-align: center; border-radius: 4px; font-size: 11px; margin-right: 6px; font-style: normal; background: rgba(255,255,255,0.06); color: #6b8ab5; }
.rank1 { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #000; font-weight: 700; }
.rank2 { background: linear-gradient(135deg, #a78bfa, #8b5cf6); color: #fff; font-weight: 700; }
.rank3 { background: linear-gradient(135deg, #00d4ff, #0ea5e9); color: #fff; font-weight: 700; }
.ratio-bar { width: 50px; height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; display: inline-block; margin-right: 6px; vertical-align: middle; }
.ratio-bar span { display: block; height: 100%; background: linear-gradient(90deg, #00d4ff, #0ea5e9); border-radius: 2px; }

/* ===== 图表区域 ===== */
.middle-section { display: flex; gap: 14px; flex: 1; min-height: 0; }
.trend-panel { flex: 1.3; }
.channel-panel { flex: 1; }
.legend { font-size: 11px; color: #6b8ab5; font-weight: normal; display: flex; align-items: center; gap: 12px; }
.legend .dot { width: 10px; height: 3px; display: inline-block; margin-right: 4px; }
.legend .dot.blue { background: #00d4ff; }
.legend .dot.dashed { background: repeating-linear-gradient(90deg, #a78bfa, #a78bfa 4px, transparent 4px, transparent 6px); height: 2px; width: 14px; }
.chart-box { width: 100%; height: 100%; min-height: 0; }
.donut { height: 180px; }
.channel-wrap { display: flex; height: calc(100% - 35px); }
.channel-list { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 12px; padding-left: 10px; }
.channel-item { display: flex; align-items: center; font-size: 12px; }
.channel-item .dot { width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; flex-shrink: 0; }
.channel-item .name { flex: 1; color: #6b8ab5; }
.channel-item .value { width: 70px; color: #e2e8f0; text-align: right; font-variant-numeric: tabular-nums; }
.channel-item .ratio { width: 45px; color: #00d4ff; text-align: right; font-weight: 600; }

/* ===== 关键指标 ===== */
.key-metrics { display: flex; gap: 10px; flex-shrink: 0; }
.metric-card {
  flex: 1; background: linear-gradient(135deg, rgba(12,26,58,0.8), rgba(8,18,46,0.9));
  border-radius: 10px; border: 1px solid rgba(0,212,255,0.1);
  padding: 12px; display: flex; gap: 10px; transition: all 0.3s;
  backdrop-filter: blur(10px);
}
.metric-card:hover { border-color: rgba(0,212,255,0.3); box-shadow: 0 0 20px rgba(0,212,255,0.1); transform: translateY(-2px); }
.metric-icon {
  width: 36px; height: 36px; background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(0,212,255,0.05));
  border-radius: 8px; display: flex; align-items: center; justify-content: center;
  color: #00d4ff; font-size: 16px; flex-shrink: 0; border: 1px solid rgba(0,212,255,0.15);
}
.metric-body { flex: 1; min-width: 0; }
.metric-label { color: #6b8ab5; font-size: 11px; }
.metric-value { font-size: 18px; font-weight: 700; margin: 2px 0; color: #fff; font-variant-numeric: tabular-nums; }
.metric-change { font-size: 11px; display: flex; align-items: center; gap: 2px; }
.metric-change.up { color: #34d399; }
.metric-change.down { color: #f87171; }

/* ===== 底部控制栏 ===== */
.screen-footer {
  height: 44px; min-height: 44px; position: relative; z-index: 1;
  background: linear-gradient(0deg, rgba(7,13,36,0.98), rgba(10,20,50,0.95));
  border-top: 1px solid rgba(0,212,255,0.1);
  display: flex; align-items: center; justify-content: space-between; padding: 0 24px;
  color: #6b8ab5; font-size: 12px;
}
.screen-footer::before {
  content: ''; position: absolute; top: -1px; left: 50%; transform: translateX(-50%);
  width: 30%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent);
}
.ctrl-left, .ctrl-right { display: flex; gap: 15px; align-items: center; }
.play-state { color: #00d4ff; cursor: pointer; transition: color 0.2s; }
.play-state:hover { color: #5ce4ff; }
.ctrl-center { display: flex; align-items: center; gap: 16px; }
.page-dots { display: flex; gap: 8px; }
.page-dots .dot {
  width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.1);
  cursor: pointer; transition: all 0.3s;
}
.page-dots .dot.active {
  background: #00d4ff; width: 24px; border-radius: 4px;
  box-shadow: 0 0 8px rgba(0,212,255,0.5);
}
.page-dots .dot:hover:not(.active) { background: rgba(0,212,255,0.3); }
.arrow { font-size: 16px; cursor: pointer; color: #6b8ab5; transition: color 0.2s; padding: 4px; }
.arrow:hover { color: #00d4ff; }
</style>
