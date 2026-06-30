<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">会议室管理</div>
      <div class="oa-desc">会议室预约、使用记录与状态看板</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-date-picker v-model="date" type="date" placeholder="选择日期" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">预约会议室</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="room" label="会议室" />
        <el-table-column prop="theme" label="会议主题" />
        <el-table-column prop="time" label="时间段" />
        <el-table-column prop="booker" label="预约人" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">详情</el-button>
            <el-button type="text">取消</el-button>
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
      date: '',
      list: [
        { room: 'A101 大会议室', theme: '月度经营分析会', time: '09:00 - 11:00', booker: '张伟', status: '使用中', statusType: 'success' },
        { room: 'B202 小会议室', theme: '产品需求评审', time: '14:00 - 15:30', booker: '李娜', status: '已预约', statusType: 'warning' },
        { room: 'C303 视频会议室', theme: '客户远程会议', time: '16:00 - 17:00', booker: '王强', status: '已预约', statusType: 'warning' },
        { room: 'A102 接待室', theme: '面试洽谈', time: '10:00 - 11:00', booker: '赵敏', status: '空闲', statusType: 'info' }
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
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
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
