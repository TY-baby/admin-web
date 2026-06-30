<template>
  <div class="erp-page">
    <div class="erp-header">
      <div class="erp-title">人事管理</div>
      <div class="erp-desc">员工档案、考勤与薪酬</div>
    </div>

    <div class="erp-card">
      <div class="erp-toolbar">
        <el-input v-model="keyword" placeholder="姓名/工号" clearable style="width:260px" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增员工</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="code" label="工号" width="120" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="dept" label="部门" width="120" />
        <el-table-column prop="position" label="职位" width="140" />
        <el-table-column prop="phone" label="手机号" width="140" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">档案</el-button>
            <el-button type="text">考勤</el-button>
            <el-button type="text">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="erp-pagination" background layout="prev, pager, next" :total="86" />
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
        { code: 'E1001', name: '张伟', dept: '研发部', position: '高级工程师', phone: '13800138001', status: '在职', statusType: 'success' },
        { code: 'E1002', name: '李娜', dept: '财务部', position: '财务主管', phone: '13800138002', status: '在职', statusType: 'success' },
        { code: 'E1003', name: '王强', dept: '生产部', position: '车间主任', phone: '13800138003', status: '休假', statusType: 'warning' },
        { code: 'E1004', name: '赵敏', dept: '采购部', position: '采购经理', phone: '13800138004', status: '在职', statusType: 'success' }
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
  background: linear-gradient(135deg, #6366f1, #818cf8);
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
