<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">请假审批</div>
      <div class="oa-desc">请假申请、审批流与假期余额</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-input v-model="keyword" placeholder="申请人/请假类型" clearable style="width:260px" />
        <el-select v-model="status" placeholder="审批状态" clearable style="width:140px">
          <el-option label="待审批" value="pending" />
          <el-option label="已通过" value="approved" />
          <el-option label="已驳回" value="rejected" />
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">我要请假</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="code" label="申请单号" width="160" />
        <el-table-column prop="applicant" label="申请人" width="120" />
        <el-table-column prop="type" label="请假类型" width="120" />
        <el-table-column prop="range" label="请假时间" />
        <el-table-column prop="days" label="天数" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">通过</el-button>
            <el-button type="text">驳回</el-button>
            <el-button type="text">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="oa-pagination" background layout="prev, pager, next" :total="60" />
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
        { code: 'LV20260601001', applicant: '张伟', type: '年假', range: '2026-06-05 至 2026-06-06', days: 2, status: '待审批', statusType: 'warning' },
        { code: 'LV20260602002', applicant: '李娜', type: '病假', range: '2026-06-07 至 2026-06-07', days: 1, status: '已通过', statusType: 'success' },
        { code: 'LV20260603003', applicant: '王强', type: '事假', range: '2026-06-10 至 2026-06-12', days: 3, status: '已驳回', statusType: 'danger' },
        { code: 'LV20260604004', applicant: '赵敏', type: '调休', range: '2026-06-08 至 2026-06-08', days: 1, status: '待审批', statusType: 'warning' }
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
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
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
