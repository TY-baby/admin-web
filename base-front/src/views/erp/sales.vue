<template>
  <div class="erp-page">
    <div class="erp-header">
      <div class="erp-title">销售管理</div>
      <div class="erp-desc">销售订单、客户报价与发货</div>
    </div>

    <div class="erp-card">
      <div class="erp-toolbar">
        <el-input v-model="keyword" placeholder="销售单号/客户" clearable style="width:260px" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增销售单</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="code" label="销售单号" width="160" />
        <el-table-column prop="customer" label="客户" />
        <el-table-column prop="amount" label="金额" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="下单日期" width="140" />
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">详情</el-button>
            <el-button type="text">发货</el-button>
            <el-button type="text" style="color:#f56c6c">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="erp-pagination" background layout="prev, pager, next" :total="110" />
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
        { code: 'SO20260601001', customer: '华能集团', amount: '¥ 156,000', status: '已发货', statusType: 'success', date: '2026-06-01' },
        { code: 'SO20260602002', customer: '东风汽车', amount: '¥ 89,500', status: '待发货', statusType: 'warning', date: '2026-06-02' },
        { code: 'SO20260603003', customer: '中航工业', amount: '¥ 234,000', status: '审批中', statusType: 'info', date: '2026-06-03' },
        { code: 'SO20260604004', customer: '比亚迪股份', amount: '¥ 567,000', status: '已完成', statusType: 'primary', date: '2026-06-04' }
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
  background: linear-gradient(135deg, #06b6d4, #22d3ee);
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
