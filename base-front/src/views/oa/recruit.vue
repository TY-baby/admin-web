<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">招聘管理</div>
      <div class="oa-desc">招聘需求、简历库与面试安排</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-input v-model="keyword" placeholder="岗位/候选人" clearable style="width:260px" />
        <el-select v-model="status" placeholder="招聘状态" clearable style="width:140px">
          <el-option label="招聘中" value="open" />
          <el-option label="已暂停" value="pause" />
          <el-option label="已关闭" value="close" />
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增岗位</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="position" label="招聘岗位" />
        <el-table-column prop="dept" label="招聘部门" width="120" />
        <el-table-column prop="headcount" label="招聘人数" width="100" />
        <el-table-column prop="candidate" label="当前候选人" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publishDate" label="发布日期" width="140" />
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">简历</el-button>
            <el-button type="text">面试</el-button>
            <el-button type="text">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="oa-pagination" background layout="prev, pager, next" :total="40" />
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
        { position: '高级前端工程师', dept: '研发部', headcount: 2, candidate: '5', status: '招聘中', statusType: 'success', publishDate: '2026-05-20' },
        { position: '财务专员', dept: '财务部', headcount: 1, candidate: '8', status: '招聘中', statusType: 'success', publishDate: '2026-05-25' },
        { position: '销售经理', dept: '销售部', headcount: 3, candidate: '12', status: '已暂停', statusType: 'warning', publishDate: '2026-05-15' },
        { position: '行政前台', dept: '人事行政部', headcount: 1, candidate: '4', status: '已关闭', statusType: 'info', publishDate: '2026-05-10' }
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
