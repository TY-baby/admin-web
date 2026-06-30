<template>
  <div class="erp-page">
    <div class="erp-header">
      <div class="erp-title">财务管理</div>
      <div class="erp-desc">应收应付、费用报销与财务报表</div>
    </div>

    <div class="erp-card">
      <div class="erp-toolbar">
        <el-input v-model="keyword" placeholder="单据号/往来单位" clearable style="width:260px" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增收付款</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="code" label="单据号" width="160" />
        <el-table-column prop="type" label="类型" width="100" />
        <el-table-column prop="partner" label="往来单位" />
        <el-table-column prop="amount" label="金额" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="日期" width="140" />
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">核销</el-button>
            <el-button type="text">详情</el-button>
            <el-button type="text">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="erp-pagination" background layout="prev, pager, next" :total="90" />
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
        { code: 'AR20260601001', type: '应收', partner: '华能集团', amount: '¥ 156,000', status: '未收', statusType: 'warning', date: '2026-06-01' },
        { code: 'AP20260602002', type: '应付', partner: '华东钢铁', amount: '¥ 45,000', status: '已付', statusType: 'success', date: '2026-06-02' },
        { code: 'EX20260603003', type: '费用', partner: '行政部', amount: '¥ 3,200', status: '已报销', statusType: 'info', date: '2026-06-03' },
        { code: 'AR20260604004', type: '应收', partner: '比亚迪股份', amount: '¥ 567,000', status: '部分收款', statusType: 'primary', date: '2026-06-04' }
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
  background: linear-gradient(135deg, #14b8a6, #2dd4bf);
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
