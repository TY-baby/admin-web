<template>
  <screen-wrapper title="园区HSE监控">
    <div class="hse-screen">
      <div class="row row-top">
        <div class="weather-box">
          <div class="w-day"><i class="el-icon-sunny"></i><span>今天</span><em>4~12℃</em></div>
          <div class="w-day"><i class="el-icon-sunrise"></i><span>明天</span><em>6~17℃</em></div>
          <div class="w-day"><i class="el-icon-cloudy"></i><span>后天</span><em>9~22℃</em></div>
        </div>
        <div class="hse-kpis">
          <div class="hk-item"><span>工作票</span><strong>20</strong></div>
          <div class="hk-item"><span>隐患数</span><strong>717</strong></div>
        </div>
        <div class="gauge-strip">
          <div class="mini-gauge" v-for="(g, i) in gauges" :key="i">
            <div class="mg-name">{{ g.name }}</div>
            <div ref="gaugeEls" :data-index="i" class="mg-chart"></div>
            <div class="mg-value" :style="{color: g.color}">{{ g.value }}{{ g.unit }}</div>
          </div>
        </div>
      </div>

      <div class="row row-mid">
        <screen-panel title="隐患上报情况统计" class="hse-panel">
          <div ref="reportChart" class="chart-box"></div>
        </screen-panel>
        <screen-panel title="隐患整改率" class="hse-panel">
          <div ref="rectifyChart" class="chart-box"></div>
        </screen-panel>
        <screen-panel title="隐患类别" class="hse-panel">
          <div ref="categoryChart" class="chart-box"></div>
        </screen-panel>
        <screen-panel title="隐患状态" class="hse-panel">
          <div ref="statusChart" class="chart-box"></div>
        </screen-panel>
      </div>

      <div class="row row-bottom">
        <screen-panel title="作业票类型" class="hse-panel">
          <div ref="ticketTypeChart" class="chart-box"></div>
        </screen-panel>
        <screen-panel title="作业票完成情况" class="hse-panel">
          <div ref="ticketDoneChart" class="chart-box"></div>
        </screen-panel>
        <screen-panel title="实时隐患信息" class="alert-panel">
          <div class="scroll-list" ref="scrollList">
            <div class="scroll-item" v-for="(a, i) in alerts" :key="i">
              <span class="alert-time">{{ a.time }}</span>
              <span class="alert-text">{{ a.text }}</span>
            </div>
          </div>
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
      gauges: [
        { name: '应急水池液位', value: 680, unit: 'm³', min: 0, max: 2000, color: '#00d4ff' },
        { name: '热电烟囱SO₂', value: 45, unit: 'mg/m³', min: 0, max: 100, color: '#fbbf24' },
        { name: '热电烟囱NOx', value: 62, unit: 'mg/m³', min: 0, max: 150, color: '#f87171' },
        { name: '热电烟囱烟尘', value: 18, unit: 'mg/m³', min: 0, max: 50, color: '#34d399' },
        { name: '700m³应急池液位', value: 480, unit: 'm³', min: 0, max: 700, color: '#00d4ff' },
        { name: '罐区污水池液位', value: 3.2, unit: 'm', min: 0, max: 5, color: '#a78bfa' },
        { name: '铵盐酸塔PH', value: 6.8, unit: '', min: 0, max: 14, color: '#f472b6' },
        { name: '水剂吸收塔PH', value: 7.5, unit: '', min: 0, max: 14, color: '#60a5fa' }
      ],
      alerts: [
        { time: '2018-03-21 15:31:04', text: '4号精馏塔冷凝法兰泄漏，化工二厂二甲苯（氯甲烷）生产部-洪毅' },
        { time: '2018-03-21 12:53:56', text: '三硝溶解罐污水接收槽旁，脚手架是15天内未检查，剂型中心-魏光华' },
        { time: '2018-03-21 12:43:43', text: '配电室北屋面保温层上，一不锈钢管存在掉落风险，剂型中心-魏光华' },
        { time: '2018-03-21 10:53:48', text: '氯甲烷罐区边沟有积液，化工二厂二甲苯（氯甲烷）生产部-张黎华' },
        { time: '2018-03-21 10:45:46', text: '建罐管廊东边有杂物，化工二厂二甲苯（氯甲烷）生产部-张黎华' },
        { time: '2018-03-21 09:22:15', text: '环氧丙烷装车台静电接地线松动，储运部-李明' },
        { time: '2018-03-21 08:17:33', text: '消防泵房压力表读数异常，安环部-王强' }
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initGauges()
      this.initReportChart()
      this.initRectifyChart()
      this.initCategoryChart()
      this.initStatusChart()
      this.initTicketTypeChart()
      this.initTicketDoneChart()
    })
  },
  methods: {
    initGauges() {
      this.$refs.gaugeEls.forEach((el, i) => {
        const g = this.gauges[i]
        const chart = echarts.init(el)
        chart.setOption({
          series: [{
            type: 'gauge', radius: '90%', center: ['50%', '55%'],
            startAngle: 200, endAngle: -20,
            min: g.min, max: g.max,
            progress: { show: true, width: 6, itemStyle: { color: g.color } },
            axisLine: { lineStyle: { width: 6, color: [[1, 'rgba(255,255,255,0.08)']] } },
            axisTick: { show: false }, splitLine: { show: false }, axisLabel: { show: false }, pointer: { show: false },
            detail: { valueAnimation: true, fontSize: 12, fontWeight: 'bold', color: g.color, offsetCenter: [0, '10%'], formatter: '{value}' }
          }]
        })
      })
    },
    initReportChart() {
      const chart = echarts.init(this.$refs.reportChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        grid: { top: 15, right: 10, bottom: 20, left: 25, containLabel: true },
        xAxis: { type: 'category', data: ['03-05','03-08','03-12','03-15','03-19'], axisLabel: { color: '#6b8ab5', fontSize: 10 }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5', fontSize: 10 } },
        series: [
          { type: 'line', smooth: true, data: [2, 5, 3, 8, 4], lineStyle: { color: '#fbbf24', width: 2 }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(251,191,36,0.3)'},{offset:1,color:'rgba(251,191,36,0)'}] } }, itemStyle: { color: '#fbbf24' } },
          { type: 'line', smooth: true, data: [1, 3, 5, 4, 6], lineStyle: { color: '#f87171', width: 2 }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(248,113,113,0.3)'},{offset:1,color:'rgba(248,113,113,0)'}] } }, itemStyle: { color: '#f87171' } }
        ]
      })
    },
    initRectifyChart() {
      const chart = echarts.init(this.$refs.rectifyChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        grid: { top: 15, right: 10, bottom: 20, left: 25, containLabel: true },
        xAxis: { type: 'category', data: ['公司部门','化工二厂','热电','建材农药厂'], axisLabel: { color: '#6b8ab5', fontSize: 10, rotate: 20 }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', max: 100, splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5', fontSize: 10 } },
        series: [{ type: 'bar', data: [12, 85, 55, 40], barWidth: '45%', itemStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'#34d399'},{offset:1,color:'#059669'}]), borderRadius: [4,4,0,0] } }]
      })
    },
    initCategoryChart() {
      const chart = echarts.init(this.$refs.categoryChart)
      chart.setOption({
        tooltip: { trigger: 'item', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        legend: { orient: 'vertical', right: 0, top: 'center', textStyle: { color: '#6b8ab5', fontSize: 10 }, itemWidth: 8, itemHeight: 8 },
        series: [{
          type: 'pie', radius: ['50%', '70%'], center: ['35%', '50%'],
          label: { show: false },
          data: [
            { value: 568, name: '物', itemStyle: { color: '#1e3a5f' } },
            { value: 83, name: '环', itemStyle: { color: '#fbbf24' } },
            { value: 21, name: '人', itemStyle: { color: '#00d4ff' } },
            { value: 45, name: '管', itemStyle: { color: '#f472b6' } }
          ]
        }]
      })
    },
    initStatusChart() {
      const chart = echarts.init(this.$refs.statusChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        grid: { top: 15, right: 10, bottom: 20, left: 25, containLabel: true },
        xAxis: { type: 'category', data: ['整改中','未整改','未出方案','整改完毕','已出方案','核实完成'], axisLabel: { color: '#6b8ab5', fontSize: 9, rotate: 25 }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5', fontSize: 10 } },
        series: [{ type: 'bar', data: [12, 8, 15, 22, 10, 450], barWidth: '50%', itemStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'#00d4ff'},{offset:1,color:'#0ea5e9'}]), borderRadius: [4,4,0,0] } }]
      })
    },
    initTicketTypeChart() {
      const chart = echarts.init(this.$refs.ticketTypeChart)
      chart.setOption({
        tooltip: { trigger: 'item', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        series: [{
          type: 'pie', radius: '70%', center: ['50%', '50%'], label: { color: '#6b8ab5', fontSize: 10 },
          data: [
            { value: 4, name: '二厂高处作业', itemStyle: { color: '#f87171' } },
            { value: 3, name: '热电厂高处作业', itemStyle: { color: '#fbbf24' } },
            { value: 2, name: '剂型中心动火作业', itemStyle: { color: '#00d4ff' } },
            { value: 2, name: '热电厂动火作业', itemStyle: { color: '#34d399' } },
            { value: 1, name: '其他', itemStyle: { color: '#a78bfa' } }
          ]
        }]
      })
    },
    initTicketDoneChart() {
      const chart = echarts.init(this.$refs.ticketDoneChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        legend: { data: ['进行中', '已完成'], top: 0, textStyle: { color: '#6b8ab5', fontSize: 10 } },
        grid: { top: 25, right: 10, bottom: 20, left: 25, containLabel: true },
        xAxis: { type: 'category', data: ['周一','周二','周三','周四','周五'], axisLabel: { color: '#6b8ab5', fontSize: 10 }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', max: 100, splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5', fontSize: 10 } },
        series: [
          { name: '进行中', type: 'bar', stack: 'total', data: [20, 30, 25, 35, 20], itemStyle: { color: '#60a5fa' }, barWidth: '40%' },
          { name: '已完成', type: 'bar', stack: 'total', data: [30, 20, 35, 25, 40], itemStyle: { color: '#fbbf24' }, barWidth: '40%' }
        ]
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.hse-screen { display: flex; flex-direction: column; gap: 14px; height: 100%; }
.row { display: flex; gap: 14px; }
.row-top { flex: 0.8; align-items: center; }
.row-mid { flex: 1; min-height: 0; }
.row-bottom { flex: 1; min-height: 0; }

.weather-box { display: flex; gap: 10px; width: 220px; }
.w-day { flex: 1; background: rgba(255,255,255,0.03); border-radius: 10px; padding: 10px; text-align: center; }
.w-day i { font-size: 22px; color: #fbbf24; }
.w-day span { display: block; font-size: 11px; color: #6b8ab5; margin: 4px 0; }
.w-day em { font-size: 11px; color: #e2e8f0; }

.hse-kpis { display: flex; gap: 10px; margin-left: 10px; }
.hk-item { width: 90px; background: rgba(255,255,255,0.03); border-radius: 10px; padding: 10px; text-align: center; }
.hk-item span { display: block; font-size: 11px; color: #6b8ab5; }
.hk-item strong { display: block; font-size: 22px; font-weight: 800; color: #00d4ff; }

.gauge-strip { flex: 1; display: flex; gap: 10px; justify-content: space-between; }
.mini-gauge { flex: 1; background: rgba(255,255,255,0.03); border-radius: 10px; padding: 6px; text-align: center; display: flex; flex-direction: column; }
.mg-name { font-size: 10px; color: #6b8ab5; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.mg-chart { flex: 1; min-height: 60px; }
.mg-value { font-size: 13px; font-weight: 700; }

.hse-panel { flex: 1; min-width: 0; }
.alert-panel { flex: 1; min-width: 0; }

.scroll-list { height: 100%; overflow: hidden; position: relative; }
.scroll-item { display: flex; gap: 10px; padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.03); font-size: 11px; }
.alert-time { color: #00d4ff; white-space: nowrap; }
.alert-text { color: #e2e8f0; line-height: 1.5; }

.chart-box { width: 100%; height: 100%; }
</style>
