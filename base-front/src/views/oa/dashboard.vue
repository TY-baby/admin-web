<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">OA 概览</div>
      <div class="oa-desc">办公自动化核心数据与待办提醒</div>
    </div>

    <div class="oa-stat-grid">
      <div class="oa-stat-card" v-for="(s, i) in stats" :key="i">
        <div class="stat-icon"><i :class="s.icon"></i></div>
        <div class="stat-info">
          <div class="stat-value">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>
    </div>

    <div class="oa-card">
      <div class="card-title">待办事项</div>
      <el-timeline>
        <el-timeline-item v-for="(t, i) in todos" :key="i" :type="t.type" :timestamp="t.time">
          {{ t.content }}
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      stats: [
        { label: '待审批', value: '12', icon: 'el-icon-s-check' },
        { label: '今日考勤', value: '86/86', icon: 'el-icon-time' },
        { label: '会议室占用', value: '4/8', icon: 'el-icon-office-building' },
        { label: '未读公告', value: '3', icon: 'el-icon-bell' },
        { label: '待办任务', value: '18', icon: 'el-icon-s-claim' },
        { label: '在用车辆', value: '6', icon: 'el-icon-truck' }
      ],
      todos: [
        { content: '审批张伟的请假申请（事假 2 天）', time: '10:30', type: 'primary' },
        { content: '确认市场部会议室预约', time: '11:00', type: 'warning' },
        { content: '审核李娜的费用报销单', time: '14:00', type: 'success' },
        { content: '查看本月考勤异常统计', time: '16:00', type: 'info' }
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
.oa-page { padding: 20px; }
.oa-header {
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
  border-radius: 12px;
  padding: 24px;
  color: #fff;
  margin-bottom: 20px;
}
.oa-title { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.oa-desc { font-size: 14px; opacity: 0.9; }
.oa-stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}
.oa-stat-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.stat-icon {
  width: 48px; height: 48px;
  border-radius: 10px;
  background: #eff6ff;
  color: #3b82f6;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
}
.stat-value { font-size: 22px; font-weight: 700; color: #1e293b; }
.stat-label { font-size: 13px; color: #64748b; margin-top: 4px; }
.oa-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.card-title { font-size: 16px; font-weight: 700; margin-bottom: 16px; color: #1e293b; }
</style>
