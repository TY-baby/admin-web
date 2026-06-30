<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">考勤管理</div>
      <div class="oa-desc">打卡记录、排班与考勤异常处理</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-date-picker v-model="month" type="month" placeholder="选择月份" />
        <el-select v-model="dept" placeholder="部门" clearable style="width:140px">
          <el-option label="研发部" value="研发部" />
          <el-option label="销售部" value="销售部" />
          <el-option label="生产部" value="生产部" />
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-download">导出考勤</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="dept" label="部门" width="120" />
        <el-table-column prop="workDays" label="应出勤" width="100" />
        <el-table-column prop="actualDays" label="实际出勤" width="100" />
        <el-table-column prop="late" label="迟到" width="80" />
        <el-table-column prop="early" label="早退" width="80" />
        <el-table-column prop="absent" label="缺勤" width="80" />
        <el-table-column label="操作" width="160">
          <template>
            <el-button type="text">打卡明细</el-button>
            <el-button type="text">补卡</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="oa-pagination" background layout="prev, pager, next" :total="86" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      month: '',
      dept: '',
      list: [
        { name: '张伟', dept: '研发部', workDays: 22, actualDays: 22, late: 0, early: 0, absent: 0 },
        { name: '李娜', dept: '财务部', workDays: 22, actualDays: 21, late: 1, early: 0, absent: 0 },
        { name: '王强', dept: '生产部', workDays: 22, actualDays: 20, late: 0, early: 0, absent: 2 },
        { name: '赵敏', dept: '采购部', workDays: 22, actualDays: 22, late: 0, early: 1, absent: 0 }
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
  background: linear-gradient(135deg, #0ea5e9, #38bdf8);
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
