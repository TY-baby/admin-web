<template>
  <screen-wrapper title="异常管理驾驶舱">
    <div class="abnormal-screen">
      <div class="row row-top">
        <!-- 左侧 KPI -->
        <div class="kpi-cards">
          <div class="kpi-card total">
            <div class="kpi-label">今日异常总数</div>
            <div class="kpi-value">{{ kpi.total }}</div>
          </div>
          <div class="kpi-card solved">
            <div class="kpi-label">已处理异常</div>
            <div class="kpi-value">{{ kpi.solved }}</div>
          </div>
          <div class="kpi-card pending">
            <div class="kpi-label">未处理异常</div>
            <div class="kpi-value">{{ kpi.pending }}</div>
          </div>
        </div>

        <!-- 中间 3D 产线 -->
        <screen-panel title="产线实时监控" class="factory-panel">
          <div class="factory-floor">
            <div class="line-row" v-for="row in 3" :key="'row-'+row">
              <div class="line-title">产线{{ row }}</div>
              <div class="line-blocks">
                <div v-for="i in 6" :key="i" :class="['block', { abnormal: isAbnormal(row, i) }]">
                  <span class="block-id">{{ row }}-{{ i }}</span>
                  <span class="block-status" v-if="isAbnormal(row, i)">异常</span>
                </div>
              </div>
            </div>
            <div class="factory-legend">
              <span><i class="dot normal"></i> 正常</span>
              <span><i class="dot abnormal"></i> 异常</span>
            </div>
          </div>
        </screen-panel>

        <!-- 右侧报警 -->
        <screen-panel title="报警信息" class="alert-panel">
          <div class="alert-list">
            <div class="alert-item" v-for="(alert, idx) in alerts" :key="idx">
              <span class="alert-dot" :class="alert.level"></span>
              <div class="alert-content">
                <div class="alert-title">{{ alert.title }}</div>
                <div class="alert-desc">{{ alert.desc }}</div>
                <div class="alert-time">{{ alert.time }}</div>
              </div>
            </div>
          </div>
        </screen-panel>
      </div>

      <div class="row row-bottom">
        <screen-panel title="区域异常排行" class="rank-panel">
          <div class="rank-list">
            <div class="rank-item" v-for="(item, idx) in regionRank" :key="idx">
              <span class="rank-no" :class="'rank'+ (idx + 1)">{{ idx + 1 }}</span>
              <span class="rank-name">{{ item.name }}</span>
              <span class="rank-bar"><span :style="{width: item.value + '%'}"></span></span>
              <span class="rank-val">{{ item.value }}</span>
            </div>
          </div>
        </screen-panel>

        <screen-panel title="XX异常情况" class="mixed-panel">
          <div ref="mixedChart" class="chart-box"></div>
        </screen-panel>

        <screen-panel title="七日异常数" class="trend-panel">
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
      kpi: { total: 10, solved: 5, pending: 5 },
      abnormalSet: new Set(['1-2', '1-5', '2-3', '3-1', '3-6']),
      alerts: [
        { level: 'high', title: '设备H2传输过快', desc: '设备温度升高至40℃，预警值error', time: '09:12:03' },
        { level: 'high', title: '产线1-2停机', desc: '设备温度升高至40℃，预警值error', time: '09:08:21' },
        { level: 'mid', title: '产线2-3流量异常', desc: '流量传感器检测到异常波动', time: '08:55:47' },
        { level: 'mid', title: '产线3-1电压不稳', desc: '电压超过额定值的10%', time: '08:42:15' },
        { level: 'low', title: '产线3-6温度偏高', desc: '设备温度升高至38℃', time: '08:30:09' }
      ],
      regionRank: [
        { name: '分类名A', value: 92 },
        { name: '分类名B', value: 78 },
        { name: '分类名C', value: 65 },
        { name: '分类名D', value: 51 },
        { name: '分类名E', value: 38 },
        { name: '分类名F', value: 25 }
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initMixedChart()
      this.initTrendChart()
    })
  },
  methods: {
    isAbnormal(row, i) { return this.abnormalSet.has(row + '-' + i) },
    initMixedChart() {
      const chart = echarts.init(this.$refs.mixedChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        grid: { top: 30, right: 20, bottom: 30, left: 40, containLabel: true },
        xAxis: { type: 'category', data: ['类别A', '类别B', '类别C', '类别D'], axisLabel: { color: '#6b8ab5' }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: [
          { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5' } },
          { type: 'value', splitLine: { show: false }, axisLabel: { color: '#6b8ab5' } }
        ],
        series: [
          { type: 'bar', data: [120, 220, 180, 260], barWidth: '35%', itemStyle: { color: new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'#00d4ff'},{offset:1,color:'#0ea5e9'}]), borderRadius: [5,5,0,0] } },
          { type: 'line', yAxisIndex: 1, smooth: true, data: [60, 110, 90, 130], lineStyle: { color: '#fbbf24', width: 2 }, itemStyle: { color: '#fbbf24' }, symbolSize: 5 }
        ]
      })
    },
    initTrendChart() {
      const chart = echarts.init(this.$refs.trendChart)
      chart.setOption({
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(8,18,46,0.95)', borderColor: '#1e3a5f', textStyle: { color: '#e2e8f0' } },
        grid: { top: 30, right: 20, bottom: 30, left: 40, containLabel: true },
        xAxis: { type: 'category', data: ['周一','周二','周三','周四','周五','周六','周日'], axisLabel: { color: '#6b8ab5' }, axisLine: { lineStyle: { color: '#2a3a5e' } }, axisTick: { show: false } },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#1a2744', type: 'dashed' } }, axisLabel: { color: '#6b8ab5' } },
        series: [
          { type: 'line', smooth: true, data: [12, 18, 10, 22, 15, 28, 20], lineStyle: { color: '#f472b6', width: 3 }, itemStyle: { color: '#f472b6' }, areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'rgba(244,114,182,0.25)'},{offset:1,color:'rgba(244,114,182,0)'}] } } }
        ]
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.abnormal-screen { display: flex; flex-direction: column; gap: 14px; height: 100%; }
.row { display: flex; gap: 14px; }
.row-top { flex: 1.4; min-height: 0; }
.row-bottom { flex: 1; min-height: 0; }

.kpi-cards { display: flex; flex-direction: column; gap: 12px; width: 180px; flex-shrink: 0; }
.kpi-card {
  flex: 1;
  background: linear-gradient(135deg, rgba(12,26,58,0.85), rgba(8,18,46,0.95));
  border: 1px solid rgba(0,212,255,0.12);
  border-radius: 10px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 8px;
}
.kpi-label { font-size: 12px; color: #6b8ab5; }
.kpi-value { font-size: 32px; font-weight: 800; color: #fff; }
.kpi-card.total { border-color: rgba(0,212,255,0.25); .kpi-value { color: #00d4ff; } }
.kpi-card.solved { border-color: rgba(52,211,153,0.25); .kpi-value { color: #34d399; } }
.kpi-card.pending { border-color: rgba(248,113,113,0.25); .kpi-value { color: #f87171; } }

.factory-panel { flex: 1; min-width: 0; }
.factory-floor { height: 100%; display: flex; flex-direction: column; justify-content: center; padding: 10px 0; }
.line-row { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
.line-title { width: 50px; font-size: 13px; color: #6b8ab5; }
.line-blocks { flex: 1; display: flex; gap: 12px; }
.block {
  flex: 1;
  height: 60px;
  background: linear-gradient(135deg, rgba(0,212,255,0.12), rgba(0,212,255,0.04));
  border: 1px solid rgba(0,212,255,0.2);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  box-shadow: 0 0 15px rgba(0,212,255,0.1);
  transition: all 0.3s;
}
.block-id { font-size: 12px; color: #6b8ab5; }
.block-status { font-size: 11px; color: #f87171; font-weight: 700; }
.block.abnormal {
  background: linear-gradient(135deg, rgba(248,113,113,0.15), rgba(248,113,113,0.05));
  border-color: rgba(248,113,113,0.4);
  box-shadow: 0 0 15px rgba(248,113,113,0.2);
  animation: pulse 2s infinite;
}
@keyframes pulse { 0%, 100% { box-shadow: 0 0 15px rgba(248,113,113,0.2); } 50% { box-shadow: 0 0 25px rgba(248,113,113,0.4); } }

.factory-legend { display: flex; justify-content: center; gap: 24px; margin-top: 10px; color: #6b8ab5; font-size: 12px; }
.dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
.dot.normal { background: #00d4ff; }
.dot.abnormal { background: #f87171; }

.alert-panel { width: 300px; flex-shrink: 0; }
.alert-list { display: flex; flex-direction: column; gap: 10px; }
.alert-item { display: flex; gap: 10px; padding: 10px; background: rgba(255,255,255,0.03); border-radius: 8px; }
.alert-dot { width: 8px; height: 8px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.alert-dot.high { background: #f87171; box-shadow: 0 0 8px #f87171; }
.alert-dot.mid { background: #fbbf24; }
.alert-dot.low { background: #00d4ff; }
.alert-title { font-size: 13px; color: #e2e8f0; font-weight: 600; }
.alert-desc { font-size: 11px; color: #6b8ab5; margin: 3px 0; }
.alert-time { font-size: 10px; color: #475569; }

.rank-panel { flex: 1; min-width: 0; }
.rank-list { display: flex; flex-direction: column; gap: 10px; }
.rank-item { display: flex; align-items: center; gap: 10px; font-size: 12px; }
.rank-no { width: 18px; height: 18px; line-height: 18px; text-align: center; border-radius: 3px; font-size: 11px; background: rgba(255,255,255,0.06); color: #6b8ab5; }
.rank-no.rank1 { background: #fbbf24; color: #000; }
.rank-no.rank2 { background: #a78bfa; color: #fff; }
.rank-no.rank3 { background: #00d4ff; color: #fff; }
.rank-name { width: 70px; color: #e2e8f0; }
.rank-bar { flex: 1; height: 5px; background: rgba(255,255,255,0.06); border-radius: 3px; }
.rank-bar span { display: block; height: 100%; border-radius: 3px; background: linear-gradient(90deg, #00d4ff, #0ea5e9); }
.rank-val { width: 30px; color: #00d4ff; text-align: right; }

.mixed-panel { flex: 1.2; min-width: 0; }
.trend-panel { flex: 1; min-width: 0; }
.chart-box { width: 100%; height: 100%; }
</style>
