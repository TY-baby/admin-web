<template>
  <div ref="chart" :style="{ width: '100%', height: height }"></div>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'LineChart',
  props: {
    height: { type: String, default: '320px' },
    dates: { type: Array, default: () => [] },
    series: { type: Array, default: () => [] }
  },
  data() { return { chart: null } },
  watch: {
    dates() { this.render() },
    series: { deep: true, handler() { this.render() } }
  },
  mounted() {
    this.chart = echarts.init(this.$refs.chart)
    this.render()
    window.addEventListener('resize', this.resize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resize)
    if (this.chart) this.chart.dispose()
  },
  methods: {
    resize() { if (this.chart) this.chart.resize() },
    render() {
      if (!this.chart) return
      this.chart.setOption({
        tooltip: { trigger: 'axis' },
        legend: { data: this.series.map(s => s.name) },
        grid: { left: 50, right: 20, top: 40, bottom: 40 },
        xAxis: { type: 'category', boundaryGap: false, data: this.dates },
        yAxis: { type: 'value' },
        series: this.series.map(s => ({
          name: s.name, type: 'line', smooth: true, data: s.data,
          itemStyle: s.color ? { color: s.color } : {},
          areaStyle: { opacity: 0.15 }
        }))
      }, true)
    }
  }
}
</script>