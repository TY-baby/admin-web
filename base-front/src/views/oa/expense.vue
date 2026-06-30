<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">费用报销</div>
      <div class="oa-desc">报销申请、发票管理与财务核销</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-input v-model="keyword" placeholder="申请人/报销类型" clearable style="width:260px" />
        <el-select v-model="status" placeholder="状态" clearable style="width:140px">
          <el-option label="待审批" value="pending" />
          <el-option label="已通过" value="approved" />
          <el-option label="已打款" value="paid" />
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增报销</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="code" label="报销单号" width="160" />
        <el-table-column prop="applicant" label="申请人" width="120" />
        <el-table-column prop="type" label="报销类型" width="120" />
        <el-table-column prop="amount" label="金额" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="申请日期" width="140" />
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">审批</el-button>
            <el-button type="text">发票</el-button>
            <el-button type="text">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="oa-pagination" background layout="prev, pager, next" :total="70" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      keyword: '',
      status: '',
      list: [
        { code: 'EX20260601001', applicant: '张伟', type: '差旅费', amount: '¥ 1,250', status: '待审批', statusType: 'warning', date: '2026-06-01' },
        { code: 'EX20260602002', applicant: '李娜', type: '办公用品', amount: '¥ 320', status: '已通过', statusType: 'success', date: '2026-06-02' },
        { code: 'EX20260603003', applicant: '王强', type: '招待费', amount: '¥ 860', status: '已打款', statusType: 'primary', date: '2026-06-03' },
        { code: 'EX20260604004', applicant: '赵敏', type: '交通费', amount: '¥ 150', status: '待审批', statusType: 'warning', date: '2026-06-04' }
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
.oa-page { padding: 20px; }
.oa-header {
  background: linear-gradient(135deg, #14b8a6, #2dd4bf);
  border-radius: 12px;
  padding: 24px;
  color: #fff;
  margin-bottom: 20px;
}
.oa-title { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.oa-desc { font-size: 14px; opacity: 0.9; }
.oa-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.oa-toolbar { display: flex; gap: 12px; margin-bottom: 16px; }
.oa-pagination { margin-top: 16px; text-align: right; }
</style>
