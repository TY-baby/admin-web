<template>
  <screen-wrapper title="航空运营监控">
    <div class="aviation-screen">
      <div class="row row-top">
        <screen-panel title="航班概况" class="kpi-panel">
          <div class="flight-kpis">
            <div class="fk-item">
              <i class="el-icon-s-promotion fk-icon blue"></i>
              <div><span>总航班</span><strong>107</strong></div>
            </div>
            <div class="fk-item">
              <i class="el-icon-location-outline fk-icon purple"></i>
              <div><span>国际/国内</span><strong>13/94</strong></div>
            </div>
            <div class="fk-item">
              <i class="el-icon-time fk-icon cyan"></i>
              <div><span>实飞/起飞</span><strong>85/107</strong></div>
            </div>
          </div>
        </screen-panel>

        <screen-panel title="准点率/利用率" class="gauge-panel">
          <div class="gauge-row">
            <div ref="gaugeChart1" class="gauge-box"></div>
            <div ref="gaugeChart2" class="gauge-box"></div>
            <div class="flight-status">
              <div class="pie-center"><div ref="flightPie" class="pie-box"></div></div>
            </div>
          </div>
        </screen-panel>

        <screen-panel title="重点航班" class="flight-table-panel">
          <table class="av-table">
            <thead><tr><th>序号</th><th>航班号</th><th>航线</th><th>7天准点率</th><th>状态</th></tr></thead>
            <tbody>
              <tr v-for="(f, i) in focusFlights" :key="i">
                <td>{{ i + 1 }}</td><td>{{ f.no }}</td><td>{{ f.route }}</td><td>{{ f.rate }}</td>
                <td><span class="status-tag" :class="f.status">{{ f.statusText }}</span></td>
              </tr>
            </tbody>
          </table>
        </screen-panel>

        <screen-panel title="今日公司值班" class="duty-panel">
          <div class="safe-days">安全运行 <strong>138</strong> 天</div>
          <ul class="duty-list">
            <li><span>公司领导</span><strong>马云云</strong><em>8660000</em></li>
            <li><span>总负责人</span><strong>马东东</strong><em>8660123</em></li>
            <li><span>AOC</span><strong>陈管管</strong><em>8660002</em></li>
            <li><span>值班经理</span><strong>刘东东</strong><em>8660123</em></li>
            <li><span>签派带班</span><strong>陈管管</strong><em>8660002</em></li>
          </ul>
        </screen-panel>
      </div>

      <div class="row row-mid">
        <div class="info-grid">
          <div class="info-card"><i class="el-icon-s-promotion"></i><div><span>飞机</span><strong>28架</strong><em>投入运力:27</em></div></div>
          <div class="info-card"><i class="el-icon-s-custom"></i><div><span>机组</span><strong>229组</strong><em>备份:9</em></div></div>
          <div class="info-card"><i class="el-icon-s-tools"></i><div><span>机务</span><strong>180人</strong><em>投入飞行:45</em></div></div>
          <div class="info-card"><i class="el-icon-box"></i><div><span>邮货总量</span><strong>266t</strong><em>运货量:77</em></div></div>
        </div>

        <screen-panel title="延误原因" class="delay-reason-panel">
          <div class="delay-reasons">
            <div class="reason-bar" v-for="(r, i) in delayReasons" :key="i">
              <span class="r-name">{{ r.name }}</span>
              <span class="r-bar"><span :style="{width: r.percent}"></span></span>
              <span class="r-val">{{ r.value }}</span>
            </div>
          </div>
        </screen-panel>
      </div>

      <div class="row row-bottom">
        <screen-panel title="延误分析" class="delay-table-panel">
          <table class="av-table">
            <thead><tr><th>序号</th><th>外站号</th><th>航班号</th><th>航线</th><th>延误原因</th><th>预飞</th><th>实飞</th></tr></thead>
            <tbody>
              <tr v-for="(d, i) in delayList" :key="i">
                <td>{{ i + 1 }}</td><td>{{ d.station }}</td><td>{{ d.no }}</td><td>{{ d.route }}</td><td>{{ d.reason }}</td><td>{{ d.plan }}</td><td>{{ d.real }}</td>
              </tr>
            </tbody>
          </table>
        </screen-panel>

        <screen-panel title="气象云图" class="weather-panel">
          <div class="weather-img">
            <div class="cloud"></div>
            <div class="weather-info">
              <div><span>台风</span><strong>莲花</strong></div>
              <div><span>风速</span><strong>28m/s</strong></div>
              <div><span>气压</span><strong>980hPa</strong></div>
            </div>
          </div>
        </screen-panel>

        <screen-panel title="地面保障" class="ground-panel">
          <div class="ground-grid">
            <div class="g-item"><span>机位数</span><strong>41</strong></div>
            <div class="g-item"><span>作业车</span><strong>113</strong></div>
            <div class="g-item"><span>廊桥(进/出)</span><strong>123/56</strong></div>
            <div class="g-item"><span>集装器</span><strong>867</strong></div>
            <div class="g-item"><span>集装板</span><strong>1468</strong></div>
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
      focusFlights: [
        { no: 'AX001', route: '南京-福州', rate: '0.60', status: 'ground', statusText: '未飞' },
        { no: 'AX002', route: '南京-深圳', rate: '0.62', status: 'air', statusText: '空中' },
        { no: 'AX003', route: '西安-北京', rate: '0.71', status: 'air', statusText: '空中' },
        { no: 'AX004', route: '福州-杭州', rate: '0.73', status: 'protect', statusText: '保障中' },
        { no: 'AX005', route: '南京-北京', rate: '0.84', status: 'ground', statusText: '未飞' },
        { no: 'AX006', route: '南京-厦门', rate: '0.88', status: 'protect', statusText: '保障中' }
      ],
      delayReasons: [
        { name: '0-2H', value: 3, percent: '60%' },
        { name: '2-4H', value: 2, percent: '40%' },
        { name: '>4H', value: 1, percent: '20%' }
      ],
      delayList: [
        { station: '南京', no: 'AX001', route: '南京-福州', reason: '因北京严重雾霾无法降落', plan: '09:26', real: '13:30' },
        { station: '南京', no: 'AX002', route: '南京-深圳', reason: '因上海航路流控导致顺移', plan: '12:25', real: '15:30' },
        { station: '南京', no: 'AX003', route: '西安-北京', reason: '流量控制', plan: '11:56', real: '22:30' },
        { station: '南京', no: 'AX004', route: '福州-杭州', reason: '因福州天气原因', plan: '12:25', real: '19:12' },
        { station: '南京', no: 'AX005', route: '南京-北京', reason: '因南京流控控制', plan: '06:20', real: '13:30' }
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initGauge(this.$refs.gaugeChart1, '航班正点率', 88, '#00d4ff')
      this.initGauge(this.$refs.gaugeChart2, '飞机利用率', 84, '#fbbf24')
      this.initPie()
    })
  },
  methods: {
    initGauge(ref, name, value, color) {
      const chart = echarts.init(ref)
      chart.setOption({
        series: [{
          type: 'gauge', startAngle: 200, endAngle: -20,
          radius: '90%', center: ['50%', '55%'],
          progress: { show: true, width: 10, itemStyle: { color: color } },
          axisLine: { lineStyle: { width: 10, color: [[1, 'rgba(255,255,255,0.08)']] } },
          axisTick: { show: false }, splitLine: { show: false }, axisLabel: { show: false },
          pointer: { show: false },
          detail: { valueAnimation: true, fontSize: 22, fontWeight: 'bold', color: '#e2e8f0', offsetCenter: [0, '10%'], formatter: '{value}%' },
          data: [{ value: value, name: name }],
          title: { offsetCenter: [0, '55%'], fontSize: 10, color: '#6b8ab5' }
        }]
      })
    },
    initPie() {
      const chart = echarts.init(this.$refs.flightPie)
      chart.setOption({
        color: ['#00d4ff', '#fbbf24', '#f87171', '#34d399'],
        tooltip: { trigger: 'item', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        series: [{
          type: 'pie', radius: ['55%', '75%'], center: ['50%', '50%'], avoidLabelOverlap: false,
          label: { show: true, position: 'outside', color: '#6b8ab5', fontSize: 10, formatter: '{b}\n{d}%' },
          data: [{name:'正常',value:85},{name:'延误',value:12},{name:'取消',value:2},{name:'返航',value:1}]
        }]
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.aviation-screen { display: flex; flex-direction: column; gap: 14px; height: 100%; }
.row { display: flex; gap: 14px; }
.row-top { flex: 1.4; min-height: 0; }
.row-mid { flex: 0.6; min-height: 0; }
.row-bottom { flex: 1.4; min-height: 0; }

.kpi-panel { width: 16%; }
.flight-kpis { display: flex; flex-direction: column; gap: 14px; justify-content: center; height: 100%; }
.fk-item { display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; }
.fk-icon { font-size: 22px; }
.fk-icon.blue { color: #00d4ff; }
.fk-icon.purple { color: #a78bfa; }
.fk-icon.cyan { color: #34d399; }
.fk-item div { display: flex; flex-direction: column; }
.fk-item span { font-size: 11px; color: #6b8ab5; }
.fk-item strong { font-size: 16px; color: #e2e8f0; }

.gauge-panel { flex: 1; min-width: 0; }
.gauge-row { display: flex; height: 100%; align-items: center; justify-content: space-around; }
.gauge-box { width: 130px; height: 130px; }
.pie-box { width: 130px; height: 130px; }

.flight-table-panel { width: 26%; min-width: 0; }
.av-table { width: 100%; font-size: 11px; color: #e2e8f0; border-collapse: collapse; }
.av-table th { color: #6b8ab5; padding: 6px 4px; text-align: center; border-bottom: 1px solid rgba(0,212,255,0.1); }
.av-table td { padding: 6px 4px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.03); }
.status-tag { padding: 1px 6px; border-radius: 3px; font-size: 10px; }
.status-tag.ground { background: rgba(107,138,181,0.15); color: #6b8ab5; }
.status-tag.air { background: rgba(0,212,255,0.15); color: #00d4ff; }
.status-tag.protect { background: rgba(251,191,36,0.15); color: #fbbf24; }

.duty-panel { width: 18%; }
.safe-days { text-align: center; font-size: 13px; color: #e2e8f0; margin-bottom: 12px; }
.safe-days strong { font-size: 26px; color: #f87171; margin: 0 4px; }
.duty-list { list-style: none; padding: 0; margin: 0; }
.duty-list li { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.03); font-size: 11px; }
.duty-list span { color: #6b8ab5; }
.duty-list strong { color: #e2e8f0; }
.duty-list em { color: #00d4ff; font-style: normal; }

.info-grid { display: flex; gap: 14px; flex: 1; }
.info-card { flex: 1; background: rgba(255,255,255,0.03); border-radius: 10px; display: flex; align-items: center; gap: 12px; padding: 14px; }
.info-card i { font-size: 28px; color: #00d4ff; }
.info-card div { display: flex; flex-direction: column; gap: 2px; }
.info-card span { font-size: 11px; color: #6b8ab5; }
.info-card strong { font-size: 16px; color: #e2e8f0; }
.info-card em { font-size: 10px; color: #475569; }

.delay-reason-panel { width: 35%; }
.delay-reasons { display: flex; flex-direction: column; gap: 10px; justify-content: center; height: 100%; }
.reason-bar { display: flex; align-items: center; gap: 8px; font-size: 12px; }
.r-name { width: 50px; color: #6b8ab5; }
.r-bar { flex: 1; height: 8px; background: rgba(255,255,255,0.06); border-radius: 4px; }
.r-bar span { display: block; height: 100%; border-radius: 4px; background: linear-gradient(90deg, #fbbf24, #f87171); }
.r-val { width: 20px; color: #e2e8f0; text-align: right; }

.delay-table-panel { flex: 1.3; min-width: 0; }
.weather-panel { width: 22%; }
.weather-img { height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; }
.cloud { width: 120px; height: 80px; background: radial-gradient(circle at 30% 40%, #94a3b8, #475569); border-radius: 50px; position: relative; }
.cloud::before, .cloud::after { content: ''; position: absolute; background: inherit; border-radius: 50%; }
.cloud::before { width: 60px; height: 60px; top: -30px; left: 20px; }
.cloud::after { width: 70px; height: 70px; top: -25px; right: 20px; }
.weather-info { display: flex; gap: 12px; }
.weather-info div { text-align: center; }
.weather-info span { display: block; font-size: 11px; color: #6b8ab5; }
.weather-info strong { font-size: 14px; color: #e2e8f0; }

.ground-panel { width: 18%; }
.ground-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.g-item { background: rgba(255,255,255,0.03); border-radius: 8px; padding: 12px; text-align: center; }
.g-item span { display: block; font-size: 11px; color: #6b8ab5; }
.g-item strong { display: block; margin-top: 4px; font-size: 16px; color: #00d4ff; }
</style>
