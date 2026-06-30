<template>
  <div class="erp-page">
    <div class="erp-header">
      <div class="erp-title">报表中心</div>
      <div class="erp-desc">ERP 业务报表与经营分析</div>
    </div>

    <div class="erp-card">
      <div class="erp-toolbar">
        <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-download">导出报表</el-button>
      </div>

      <div class="report-grid">
        <div class="report-item" v-for="(r, i) in reports" :key="i">
          <div class="report-name">{{ r.name }}</div>
          <div class="report-desc">{{ r.desc }}</div>
          <el-button type="text">查看报表</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dateRange: [],
      reports: [
        { name: '采购分析报表', desc: '按供应商、物料、时间维度统计采购金额与数量' },
        { name: '库存周转报表', desc: '库存周转率、呆滞料预警与库龄分析' },
        { name: '生产销售报表', desc: '生产完工率、销售业绩趋势与订单交付率' },
        { name: '财务报表', desc: '应收应付汇总、现金流与利润表' },
        { name: '人事考勤报表', desc: '出勤率、加班统计与薪酬汇总' },
        { name: '经营驾驶舱', desc: '综合经营指标可视化大屏' }
      ]
    }
  },
  methods: {
    load() {
      this.$message.success('报表数据已刷新')
    }
  }
}
</script>

<style lang="scss" scoped>
.erp-page { padding: 20px; }
.erp-header {
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  border-radius: 12px;
  padding: 24px;
  color: #fff;
  margin-bottom: 20px;
}
.erp-title { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.erp-desc { font-size: 14px; opacity: 0.9; }
.erp-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.erp-toolbar { display: flex; gap: 12px; margin-bottom: 16px; }
.report-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}
.report-item {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 18px;
  transition: all 0.2s;
  &:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.06); border-color: #c7d2fe; }
}
.report-name { font-size: 16px; font-weight: 700; color: #1e293b; margin-bottom: 8px; }
.report-desc { font-size: 13px; color: #64748b; margin-bottom: 12px; line-height: 1.6; }
</style>
