<template>
  <div class="big-screen" ref="screenRef">
    <header class="screen-header">
      <div class="header-left">
        <h1 class="title">鲸跃会展轮播大屏</h1>
        <el-button class="switch-btn" size="mini" round>轮播切换大屏</el-button>
      </div>
      <div class="header-tabs">
        <div v-for="tab in tabs" :key="tab"
             :class="['tab-item', { active: activeTab === tab }]"
             @click="switchTab(tab)">
          <i :class="tabIcon[tab]"></i> {{ tab }}
        </div>
      </div>
      <div class="header-right">
        <span class="time">{{ currentTime }}</span>
        <span class="fullscreen" @click="toggleFull"><i class="el-icon-full-screen"></i> 全屏模式</span>
      </div>
    </header>

    <main class="screen-main">
      <transition name="fade-slide" mode="out-in">
        <!-- 销售 Tab -->
        <div v-if="activeTab === '销售'" key="sales" class="tab-content">
          <section class="top-section">
            <div class="panel sales-overview">
              <div class="panel-title"><span>销售总览</span><i class="el-icon-warning-outline"></i></div>
              <div class="overview-cards">
                <div class="ov-card" v-for="(c, i) in overview" :key="i">
                  <div class="ov-icon" :style="{background: c.bg}"><i :class="c.icon"></i></div>
                  <div class="ov-info">
                    <div class="ov-label">{{ c.label }}</div>
                    <div class="ov-value">{{ c.value }}</div>
                    <div class="ov-change" :class="c.change.startsWith('+') ? 'up' : 'down'">较昨日 {{ c.change }}</div>
                  </div>
                </div>
              </div>
            </div>
            <div class="panel top5-panel">
              <div class="panel-title"><span>销售额 TOP5 展会</span><span class="more">更多</span></div>
              <div class="top5-table">
                <div class="th"><span>展会名称</span><span>销售额（元）</span><span>占比</span></div>
                <div class="tr" v-for="(row, idx) in topExhibitions" :key="idx">
                  <span><span :class="['rank', 'rank' + (idx + 1)]">{{ idx + 1 }}</span>{{ row.name }}</span>
                  <span>{{ row.value }}万</span>
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
                <div class="metric-change" :class="String(m.change).startsWith('+') ? 'up' : 'down'">较昨日 {{ m.change }}</div>
                <div class="sparkline">
                  <svg viewBox="0 0 120 30" preserveAspectRatio="none">
                    <polyline :points="sparkPoints(m.spark)" fill="none"
                              :stroke="String(m.change).startsWith('+') ? '#67C23A' : '#F56C6C'" stroke-width="2" />
                  </svg>
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
        <span class="ctrl-label">轮播控制</span>
        <span class="play-state" @click="autoPlay = !autoPlay">
          <i :class="autoPlay ? 'el-icon-video-pause' : 'el-icon-video-play'"></i>
          {{ autoPlay ? '自动播放中' : '已暂停' }}
        </span>
      </div>
      <div class="ctrl-center">
        <span>当前页面</span>
        <span class="page-num">{{ currentPage }} / {{ totalPages }}</span>
        <i class="el-icon-arrow-left arrow" @click="prevTab"></i>
        <i :class="autoPlay ? 'el-icon-video-pause' : 'el-icon-video-play'" class="pause" @click="autoPlay = !autoPlay"></i>
        <i class="el-icon-arrow-right arrow" @click="nextTab"></i>
      </div>
      <div class="ctrl-right">
        <span>播放间隔 {{ autoPlayInterval }}s</span>
        <span>切换效果 滑动</span>
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
      channelColors: ['#6366f1', '#ec4899', '#f59e0b', '#06b6d4', '#10b981'],
      charts: []
    }
  },
  computed: {
    currentPage() { return this.tabs.indexOf(this.activeTab) + 1 },
    totalPages() { return this.tabs.length },
    overview() {
      const s = this.stats
      return [
        { label: '销售额（元）', value: s.totalAmount ? s.totalAmount + '万' : '8,756.32万', change: '+8.6%', icon: 'el-icon-money', bg: 'linear-gradient(135deg,#6366f1,#818cf8)' },
        { label: '订单量（笔）', value: s.totalOrders || '23,856', change: '+6.3%', icon: 'el-icon-s-order', bg: 'linear-gradient(135deg,#06b6d4,#22d3ee)' },
        { label: '客单价（元）', value: s.avgPrice || '987.12', change: '+5.6%', icon: 'el-icon-user', bg: 'linear-gradient(135deg,#f59e0b,#fbbf24)' },
        { label: '转化率', value: (s.convertRate || '3.62') + '%', change: '+0.42pt', icon: 'el-icon-data-line', bg: 'linear-gradient(135deg,#ec4899,#f472b6)' }
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
      // 等待 v-if 切换 + transition(out-in 0.4s) 完成后再初始化图表
      clearTimeout(this._tabTimer)
      this._tabTimer = setTimeout(() => {
        this.initTabCharts()
        // resize所有已存在的图表
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
    // 立即用默认数据渲染图表，不等待API
    this.$nextTick(() => this.initTabCharts())
    // 后台加载数据，成功后更新图表
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
      // 3秒超时，不阻塞页面渲染
      const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 3000))
      Promise.race([getStats(), timeout]).then(data => {
        this.stats = data
        this.$nextTick(() => this.initTabCharts())
      }).catch(() => {
        console.warn('数据加载超时，使用默认数据')
      })
    },
    switchTab(tab) {
      this.activeTab = tab
    },
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
    handleResize() {
      this.charts.forEach(c => c && c.resize())
    },
    sparkPoints(arr) {
      const data = (arr || []).map((v, i) => [i * 10, 30 - v / 5].join(','))
      return data.join(' ')
    },
    makeChart(ref) {
      const el = this.$refs[ref]
      if (!el) return null
      // Clean up stale chart instances (DOM may have been destroyed by v-if)
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
      if (this.activeTab === '销售') {
        this.initTrendChart()
        this.initChannelChart()
      } else if (this.activeTab === '用户') {
        this.initUserCharts()
      } else if (this.activeTab === '商品') {
        this.initProductCharts()
      } else if (this.activeTab === '订单') {
        this.initOrderCharts()
      } else if (this.activeTab === '财务') {
        this.initFinanceCharts()
      }
    },

    initTrendChart() {
      const chart = this.makeChart('trendChart')
      if (!chart) return
      const x = (this.stats.amountTrend || []).map(i => i.date)
      const y1 = (this.stats.amountTrend || []).map(i => i.value * 1000)
      const y2 = y1.map(v => v * 0.9)
      chart.setOption({
        grid: { top: 30, right: 20, bottom: 30, left: 50, containLabel: true },
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(15,23,42,0.9)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        xAxis: { type: 'category', data: x.length ? x : ['06-19','06-20','06-21','06-22','06-23','06-24','06-25'], axisLine: { lineStyle: { color: '#4c5b70' } }, axisLabel: { color: '#8fa2b5' }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d', type: 'dashed' } }, axisLabel: { color: '#8fa2b5', formatter: v => v >= 1000 ? (v/1000) + 'k' : v }, axisLine: { show: false } },
        series: [
          { name: '销售额', type: 'line', smooth: true, data: y1.length ? y1 : [120000,220000,380000,520000,680000,850000,920000],
            lineStyle: { color: '#6366f1', width: 3, shadowColor: 'rgba(99,102,241,0.5)', shadowBlur: 12 },
            areaStyle: { color: { type: 'linear', x:0,y:0,x2:0,y2:1, colorStops:[{offset:0,color:'rgba(99,102,241,0.4)'},{offset:1,color:'rgba(99,102,241,0)'}] } },
            itemStyle: { color: '#6366f1' }, symbolSize: 6 },
          { name: '较昨日', type: 'line', smooth: true, data: y2.length ? y2 : [110000,200000,340000,480000,600000,720000,800000],
            lineStyle: { color: '#ec4899', width: 2, type: 'dashed' }, itemStyle: { color: '#ec4899' }, symbolSize: 4 }
        ],
        animationDuration: 1200, animationEasing: 'cubicOut'
      })
    },

    initChannelChart() {
      const chart = this.makeChart('channelChart')
      if (!chart) return
      const data = this.channelData.map((c, i) => ({ name: c.name, value: c.ratio, itemStyle: { color: this.channelColors[i] } }))
      chart.setOption({
        tooltip: { trigger: 'item', backgroundColor: 'rgba(15,23,42,0.9)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        series: [{ type: 'pie', radius: ['50%', '72%'], center: ['50%', '50%'], label: { show: false },
          emphasis: { label: { show: true, color: '#e2e8f0', fontWeight: 'bold' }, itemStyle: { shadowBlur: 20, shadowColor: 'rgba(0,0,0,0.3)' } },
          itemStyle: { borderRadius: 4, borderColor: '#020617', borderWidth: 2 },
          data: data.length ? data : [{value:37,name:'展会现场'},{value:25,name:'线上商城'},{value:18,name:'代理分销'},{value:12,name:'企业直销'},{value:8,name:'其他'}]
        }],
        animationDuration: 1200
      })
    },

    initUserCharts() {
      const trend = this.makeChart('userTrendChart')
      if (trend) {
        trend.setOption({
          grid: { top: 20, right: 20, bottom: 25, left: 40 },
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: ['周一','周二','周三','周四','周五','周六','周日'], axisLabel: { color: '#8fa2b5' }, axisLine: { lineStyle: { color: '#334155' } } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d', type: 'dashed' } }, axisLabel: { color: '#8fa2b5' } },
          series: [
            { name: '新增用户', type: 'bar', data: [45,62,38,71,55,89,67], itemStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'#818cf8'},{offset:1,color:'#6366f1'}]), borderRadius: [4,4,0,0] }, barWidth: '40%' },
            { name: '活跃用户', type: 'line', smooth: true, data: [320,380,350,420,390,510,480], lineStyle: { color: '#ec4899', width: 2 }, itemStyle: { color: '#ec4899' }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(236,72,153,0.3)'},{offset:1,color:'rgba(236,72,153,0)'}] } } }
          ]
        })
      }
      const source = this.makeChart('userSourceChart')
      if (source) {
        source.setOption({
          tooltip: { trigger: 'item' },
          color: ['#6366f1','#ec4899','#f59e0b','#06b6d4','#10b981'],
          series: [{ type: 'pie', radius: '65%', roseType: 'area', label: { color: '#8fa2b5', fontSize: 11 },
            itemStyle: { borderRadius: 5, borderColor: '#020617', borderWidth: 2 },
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
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d', type: 'dashed' } }, axisLabel: { color: '#8fa2b5' } },
          yAxis: { type: 'category', data: names.reverse(), axisLabel: { color: '#e2e8f0', fontSize: 12 }, axisLine: { show: false }, axisTick: { show: false } },
          series: [{ type: 'bar', data: vals.reverse().map((v,i) => ({value:v, itemStyle: { color: new echarts.graphic.LinearGradient(0,0,1,0,[{offset:0,color:['#06b6d4','#6366f1','#ec4899','#f59e0b','#10b981'][i%5]},{offset:1,color:['#22d3ee','#818cf8','#f472b6','#fbbf24','#34d399'][i%5]}]), borderRadius:[0,4,4,0] }})), barWidth: '50%',
            label: { show: true, position: 'right', color: '#e2e8f0', fontSize: 12 }
          }]
        })
      }
    },

    initProductCharts() {
      const rank = this.makeChart('productRankChart')
      if (rank) {
        rank.setOption({
          grid: { top: 10, right: 20, bottom: 25, left: 40 },
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: ['CRM标准版','CRM高级版','数据大屏','实施服务','定制开发'], axisLabel: { color: '#8fa2b5', rotate: 15 }, axisLine: { lineStyle: { color: '#334155' } } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d', type: 'dashed' } }, axisLabel: { color: '#8fa2b5' } },
          series: [{ type: 'bar', data: [156,98,72,45,32].map((v,i) => ({value:v, itemStyle:{color:['#6366f1','#818cf8','#ec4899','#f59e0b','#06b6d4'][i]}})), barWidth: '45%', itemStyle: { borderRadius: [5,5,0,0] },
            label: { show: true, position: 'top', color: '#e2e8f0', fontSize: 12 }
          }]
        })
      }
      const cat = this.makeChart('productCatChart')
      if (cat) {
        cat.setOption({
          tooltip: { trigger: 'item' },
          color: ['#6366f1','#ec4899','#f59e0b','#06b6d4','#10b981'],
          series: [{ type: 'pie', radius: ['40%','70%'], label: { color: '#8fa2b5' },
            itemStyle: { borderRadius: 5, borderColor: '#020617', borderWidth: 2 },
            data: [{name:'软件',value:68},{name:'服务',value:18},{name:'硬件',value:8},{name:'培训',value:4},{name:'其他',value:2}]
          }]
        })
      }
      const stock = this.makeChart('productStockChart')
      if (stock) {
        stock.setOption({
          grid: { top: 30, right: 20, bottom: 30, left: 50 },
          tooltip: { trigger: 'axis' },
          legend: { data: ['入库','出库','库存'], top: 0, textStyle: { color: '#8fa2b5' } },
          xAxis: { type: 'category', data: ['1月','2月','3月','4月','5月','6月'], axisLabel: { color: '#8fa2b5' }, axisLine: { lineStyle: { color: '#334155' } } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d', type: 'dashed' } }, axisLabel: { color: '#8fa2b5' } },
          series: [
            { name: '入库', type: 'bar', data: [120,150,90,180,130,160], itemStyle: { color: '#6366f1', borderRadius: [4,4,0,0] }, barWidth: '25%' },
            { name: '出库', type: 'bar', data: [100,130,110,160,120,140], itemStyle: { color: '#ec4899', borderRadius: [4,4,0,0] }, barWidth: '25%' },
            { name: '库存', type: 'line', smooth: true, data: [500,520,500,520,530,550], lineStyle: { color: '#f59e0b', width: 2 }, itemStyle: { color: '#f59e0b' }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(245,158,11,0.2)'},{offset:1,color:'rgba(245,158,11,0)'}] } } }
          ]
        })
      }
    },

    initOrderCharts() {
      const trend = this.makeChart('orderTrendChart')
      if (trend) {
        trend.setOption({
          grid: { top: 20, right: 20, bottom: 25, left: 40 },
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: ['周一','周二','周三','周四','周五','周六','周日'], axisLabel: { color: '#8fa2b5' }, axisLine: { lineStyle: { color: '#334155' } } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d', type: 'dashed' } }, axisLabel: { color: '#8fa2b5' } },
          series: [
            { type: 'bar', data: [28,35,22,41,38,52,45].map((v,i) => ({value:v, itemStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'#818cf8'},{offset:1,color:'#6366f1'}])}})), barWidth: '40%', itemStyle: { borderRadius: [5,5,0,0] } }
          ]
        })
      }
      const status = this.makeChart('orderStatusChart')
      if (status) {
        status.setOption({
          tooltip: { trigger: 'item' },
          color: ['#6366f1','#10b981','#f59e0b','#06b6d4','#ec4899','#94a3b8'],
          series: [{ type: 'pie', radius: ['40%','70%'], label: { color: '#8fa2b5', fontSize: 11 },
            itemStyle: { borderRadius: 5, borderColor: '#020617', borderWidth: 2 },
            data: [{name:'待确认',value:18},{name:'已确认',value:25},{name:'生产中',value:15},{name:'已发货',value:22},{name:'已完成',value:38},{name:'已取消',value:5}]
          }]
        })
      }
      const amount = this.makeChart('orderAmountChart')
      if (amount) {
        amount.setOption({
          grid: { top: 30, right: 20, bottom: 30, left: 50 },
          tooltip: { trigger: 'axis', formatter: p => p[0].name + '<br/>金额: ¥' + p[0].value.toLocaleString() },
          xAxis: { type: 'category', data: ['周一','周二','周三','周四','周五','周六','周日'], axisLabel: { color: '#8fa2b5' }, axisLine: { lineStyle: { color: '#334155' } } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d', type: 'dashed' } }, axisLabel: { color: '#8fa2b5', formatter: v => v >= 10000 ? (v/10000) + 'w' : v } },
          series: [
            { type: 'line', smooth: true, data: [32000,45000,28000,62000,51000,78000,65000],
              lineStyle: { color: '#ec4899', width: 3, shadowColor: 'rgba(236,72,153,0.4)', shadowBlur: 12 },
              itemStyle: { color: '#ec4899', borderWidth: 3, borderColor: '#fff' }, symbolSize: 8,
              areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(236,72,153,0.35)'},{offset:1,color:'rgba(236,72,153,0)'}] } }
            }
          ]
        })
      }
    },

    initFinanceCharts() {
      const income = this.makeChart('incomeTrendChart')
      if (income) {
        income.setOption({
          grid: { top: 20, right: 20, bottom: 25, left: 50 },
          tooltip: { trigger: 'axis' },
          xAxis: { type: 'category', data: ['1月','2月','3月','4月','5月','6月'], axisLabel: { color: '#8fa2b5' }, axisLine: { lineStyle: { color: '#334155' } } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d', type: 'dashed' } }, axisLabel: { color: '#8fa2b5', formatter: v => (v/10000) + 'w' } },
          series: [
            { type: 'bar', data: [180000,220000,195000,260000,310000,285000].map((v,i) => ({value:v, itemStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'#34d399'},{offset:1,color:'#10b981'}])}})), barWidth: '40%', itemStyle: { borderRadius: [5,5,0,0] } }
          ]
        })
      }
      const expense = this.makeChart('expenseChart')
      if (expense) {
        expense.setOption({
          tooltip: { trigger: 'item' },
          color: ['#6366f1','#ec4899','#f59e0b','#06b6d4','#10b981'],
          series: [{ type: 'pie', radius: '65%', label: { color: '#8fa2b5' },
            itemStyle: { borderRadius: 5, borderColor: '#020617', borderWidth: 2 },
            data: [{name:'人力成本',value:42},{name:'运营费用',value:25},{name:'营销推广',value:18},{name:'技术投入',value:10},{name:'其他',value:5}]
          }]
        })
      }
      const profit = this.makeChart('profitChart')
      if (profit) {
        profit.setOption({
          grid: { top: 30, right: 20, bottom: 30, left: 50 },
          tooltip: { trigger: 'axis' },
          legend: { data: ['收入','支出','利润'], top: 0, textStyle: { color: '#8fa2b5' } },
          xAxis: { type: 'category', data: ['1月','2月','3月','4月','5月','6月'], axisLabel: { color: '#8fa2b5' }, axisLine: { lineStyle: { color: '#334155' } } },
          yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1f2d3d', type: 'dashed' } }, axisLabel: { color: '#8fa2b5', formatter: v => (v/10000) + 'w' } },
          series: [
            { name: '收入', type: 'bar', data: [180000,220000,195000,260000,310000,285000], itemStyle: { color: '#6366f1', borderRadius: [4,4,0,0] }, barWidth: '20%' },
            { name: '支出', type: 'bar', data: [120000,140000,130000,160000,180000,170000], itemStyle: { color: '#ec4899', borderRadius: [4,4,0,0] }, barWidth: '20%' },
            { name: '利润', type: 'line', smooth: true, data: [60000,80000,65000,100000,130000,115000], lineStyle: { color: '#10b981', width: 3 }, itemStyle: { color: '#10b981' }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(16,185,129,0.3)'},{offset:1,color:'rgba(16,185,129,0)'}] } }, symbolSize: 6 }
          ]
        })
      }
    }
  }
}
</script>

<style scoped>
.big-screen { width: 100vw; height: 100vh; background: #020617; color: #fff; overflow: hidden; display: flex; flex-direction: column; font-family: 'Microsoft YaHei', sans-serif; }
.screen-header { height: 60px; min-height: 60px; background: linear-gradient(90deg, rgba(8,26,56,0.95), rgba(13,42,90,0.95), rgba(8,26,56,0.95)); display: flex; align-items: center; justify-content: space-between; padding: 0 20px; border-bottom: 2px solid #1e3a5f; position: relative; }
.title { font-size: 22px; font-weight: bold; margin: 0; background: linear-gradient(90deg, #fff, #409EFF); -webkit-background-clip: text; color: transparent; }
.header-left { display: flex; align-items: center; gap: 12px; }
.switch-btn { background: rgba(64,158,255,0.2); border-color: #409EFF; color: #409EFF; font-size: 12px; }
.header-tabs { position: absolute; left: 50%; transform: translateX(-50%); display: flex; gap: 6px; }
.tab-item { padding: 6px 18px; border-radius: 4px; cursor: pointer; color: #8fa2b5; background: rgba(255,255,255,0.05); transition: all 0.3s ease; font-size: 13px; }
.tab-item:hover { background: rgba(64,158,255,0.15); color: #c0d0e0; }
.tab-item.active { background: linear-gradient(180deg, rgba(64,158,255,0.3), rgba(64,158,255,0.1)); color: #fff; border-bottom: 2px solid #409EFF; box-shadow: 0 0 15px rgba(64,158,255,0.4); }
.header-right { display: flex; align-items: center; gap: 16px; color: #8fa2b5; font-size: 13px; }
.time { font-size: 14px; }
.fullscreen { cursor: pointer; color: #409EFF; font-size: 13px; }

.screen-main { flex: 1; padding: 15px; display: flex; flex-direction: column; min-height: 0; overflow: hidden; }

/* Tab 切换动画 */
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.4s ease; }
.fade-slide-enter { opacity: 0; transform: translateX(30px); }
.fade-slide-leave-to { opacity: 0; transform: translateX(-30px); }

.tab-content { display: flex; flex-direction: column; gap: 12px; height: 100%; }

.panel { background: rgba(10,28,56,0.6); border: 1px solid #1e3a5f; border-radius: 8px; padding: 12px; box-shadow: 0 0 20px rgba(64,158,255,0.08); position: relative; }
.panel::before, .panel::after { content: ''; position: absolute; width: 10px; height: 10px; border: 2px solid #409EFF; }
.panel::before { top: -1px; left: -1px; border-right: none; border-bottom: none; border-top-left-radius: 8px; }
.panel::after { bottom: -1px; right: -1px; border-left: none; border-top: none; border-bottom-right-radius: 8px; }
.panel-title { display: flex; align-items: center; justify-content: space-between; color: #fff; font-size: 14px; font-weight: bold; margin-bottom: 10px; }
.more { color: #409EFF; font-size: 12px; cursor: pointer; }

.top-section { display: flex; gap: 15px; flex-shrink: 0; }
.sales-overview { flex: 2; }
.overview-cards { display: flex; gap: 10px; }
.ov-card { flex: 1; background: rgba(255,255,255,0.03); border-radius: 6px; padding: 10px; display: flex; align-items: center; gap: 10px; transition: all 0.3s; }
.ov-card:hover { background: rgba(255,255,255,0.06); transform: translateY(-2px); }
.ov-icon { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px; color: #fff; flex-shrink: 0; }
.ov-label { color: #8fa2b5; font-size: 11px; }
.ov-value { font-size: 20px; font-weight: bold; margin: 2px 0; }
.ov-change { font-size: 11px; }
.ov-change.up { color: #67C23A; }
.ov-change.down { color: #F56C6C; }

.top5-panel { flex: 1; overflow: hidden; }
.top5-table { font-size: 12px; }
.top5-table .th { display: flex; color: #8fa2b5; padding: 4px 0; border-bottom: 1px solid #1e3a5f; }
.top5-table .th span, .top5-table .tr span { flex: 1; text-align: center; }
.top5-table .tr { display: flex; padding: 6px 0; border-bottom: 1px solid rgba(30,58,95,0.4); align-items: center; transition: background 0.2s; }
.top5-table .tr:hover { background: rgba(64,158,255,0.05); }
.rank { display: inline-block; width: 16px; height: 16px; line-height: 16px; text-align: center; border-radius: 3px; font-size: 11px; margin-right: 6px; font-style: normal; background: #1e3a5f; }
.rank1 { background: #F7BA2A; color: #000; }
.rank2 { background: #C0C4CC; color: #000; }
.rank3 { background: #E6A23C; color: #000; }
.ratio-bar { width: 50px; height: 4px; background: #1e3a5f; border-radius: 2px; display: inline-block; margin-right: 6px; vertical-align: middle; }
.ratio-bar span { display: block; height: 100%; background: linear-gradient(90deg, #6366f1, #818cf8); border-radius: 2px; }

.middle-section { display: flex; gap: 15px; flex: 1; min-height: 0; }
.trend-panel { flex: 1.3; }
.channel-panel { flex: 1; }
.legend { font-size: 11px; color: #8fa2b5; font-weight: normal; display: flex; align-items: center; gap: 12px; }
.legend .dot { width: 10px; height: 3px; display: inline-block; margin-right: 4px; }
.legend .dot.blue { background: #6366f1; }
.legend .dot.dashed { background: repeating-linear-gradient(90deg, #ec4899, #ec4899 4px, transparent 4px, transparent 6px); height: 2px; width: 14px; }
.chart-box { width: 100%; height: 100%; min-height: 0; }
.donut { height: 180px; }
.channel-wrap { display: flex; height: calc(100% - 35px); }
.channel-list { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 10px; padding-left: 8px; }
.channel-item { display: flex; align-items: center; font-size: 12px; }
.channel-item .dot { width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; flex-shrink: 0; }
.channel-item .name { flex: 1; color: #8fa2b5; }
.channel-item .value { width: 70px; color: #fff; text-align: right; }
.channel-item .ratio { width: 45px; color: #409EFF; text-align: right; }

.key-metrics { display: flex; gap: 10px; flex-shrink: 0; }
.metric-card { flex: 1; background: rgba(10,28,56,0.6); border-radius: 8px; border: 1px solid #1e3a5f; padding: 10px; display: flex; gap: 8px; transition: all 0.3s; }
.metric-card:hover { border-color: #409EFF; box-shadow: 0 0 12px rgba(64,158,255,0.2); }
.metric-icon { width: 32px; height: 32px; background: rgba(64,158,255,0.15); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #409EFF; font-size: 16px; flex-shrink: 0; }
.metric-body { flex: 1; min-width: 0; }
.metric-label { color: #8fa2b5; font-size: 11px; }
.metric-value { font-size: 17px; font-weight: bold; margin: 2px 0; }
.metric-change { font-size: 10px; }
.metric-change.up { color: #67C23A; }
.metric-change.down { color: #F56C6C; }
.sparkline { height: 20px; margin-top: 2px; }
.sparkline svg { width: 100%; height: 100%; }

.screen-footer { height: 40px; min-height: 40px; background: rgba(10,28,56,0.8); border-top: 1px solid #1e3a5f; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; color: #8fa2b5; font-size: 12px; }
.ctrl-left, .ctrl-right { display: flex; gap: 15px; align-items: center; }
.ctrl-label { color: #fff; }
.play-state { color: #409EFF; cursor: pointer; }
.ctrl-center { display: flex; align-items: center; gap: 12px; }
.page-num { color: #fff; font-weight: bold; font-size: 14px; }
.arrow { font-size: 16px; cursor: pointer; color: #fff; transition: color 0.2s; }
.arrow:hover { color: #409EFF; }
.pause { font-size: 22px; cursor: pointer; color: #409EFF; }
</style>
