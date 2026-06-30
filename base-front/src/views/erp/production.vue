<template>
  <div class="erp-page">
    <div class="erp-header">
      <div class="erp-title">生产管理</div>
      <div class="erp-desc">生产计划、工单与进度跟踪</div>
    </div>

    <div class="erp-card">
      <div class="erp-toolbar">
        <el-input v-model="keyword" placeholder="工单号/产品名称" clearable style="width:260px" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增工单</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="code" label="工单号" width="160" />
        <el-table-column prop="product" label="产品名称" />
        <el-table-column prop="planQty" label="计划数量" width="100" />
        <el-table-column prop="finishQty" label="完成数量" width="100" />
        <el-table-column prop="progress" label="进度" width="180">
          <template slot-scope="scope">
            <el-progress :percentage="Math.round(scope.row.finishQty / scope.row.planQty * 100)" />
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">报工</el-button>
            <el-button type="text">详情</el-button>
            <el-button type="text">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="erp-pagination" background layout="prev, pager, next" :total="60" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      keyword: '',
      list: [
        { code: 'MO20260601001', product: '智能温控设备A型', planQty: 200, finishQty: 120, status: '生产中', statusType: 'primary' },
        { code: 'MO20260602002', product: '工业控制模块B2', planQty: 500, finishQty: 500, status: '已完成', statusType: 'success' },
        { code: 'MO20260603003', product: '传感器套件C1', planQty: 300, finishQty: 45, status: '待开工', statusType: 'info' },
        { code: 'MO20260604004', product: '不锈钢外壳D3', planQty: 150, finishQty: 150, status: '已结案', statusType: 'warning' }
      ]
    }
  },
  methods: {
    load() {
      this.loading = true
      setTimeout(() => { this.loading = false }, 300)
    }
  }
}
</script>

<style lang="scss" scoped>
.erp-page { padding: 20px; }
.erp-header {
  background: linear-gradient(135deg, #ec4899, #f472b6);
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
.erp-pagination { margin-top: 16px; text-align: right; }
</style>
