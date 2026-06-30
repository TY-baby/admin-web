<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">任务协作</div>
      <div class="oa-desc">任务分配、进度跟踪与团队协作</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-input v-model="keyword" placeholder="任务标题" clearable style="width:260px" />
        <el-select v-model="status" placeholder="任务状态" clearable style="width:140px">
          <el-option label="待处理" value="todo" />
          <el-option label="进行中" value="doing" />
          <el-option label="已完成" value="done" />
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新建任务</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="title" label="任务标题" />
        <el-table-column prop="assignee" label="负责人" width="120" />
        <el-table-column prop="deadline" label="截止日期" width="140" />
        <el-table-column prop="priority" label="优先级" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.priorityType" size="small">{{ scope.row.priority }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">详情</el-button>
            <el-button type="text">编辑</el-button>
            <el-button type="text">完成</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="oa-pagination" background layout="prev, pager, next" :total="90" />
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
        { title: '完成 OA 考勤模块原型设计', assignee: '张伟', deadline: '2026-06-10', priority: '高', priorityType: 'danger', status: '进行中', statusType: 'primary' },
        { title: '更新员工手册', assignee: '李娜', deadline: '2026-06-15', priority: '中', priorityType: 'warning', status: '待处理', statusType: 'info' },
        { title: '整理6月报销单据', assignee: '王强', deadline: '2026-06-08', priority: '中', priorityType: 'warning', status: '已完成', statusType: 'success' },
        { title: '会议室设备巡检', assignee: '赵敏', deadline: '2026-06-05', priority: '低', priorityType: 'info', status: '已完成', statusType: 'success' }
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
  background: linear-gradient(135deg, #06b6d4, #22d3ee);
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
