<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">通知公告</div>
      <div class="oa-desc">企业公告、制度发布与消息提醒</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-input v-model="keyword" placeholder="公告标题" clearable style="width:260px" />
        <el-select v-model="type" placeholder="公告类型" clearable style="width:140px">
          <el-option label="公司公告" value="company" />
          <el-option label="部门通知" value="dept" />
          <el-option label="制度规范" value="policy" />
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">发布公告</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="author" label="发布人" width="120" />
        <el-table-column prop="publishTime" label="发布时间" width="160" />
        <el-table-column prop="readCount" label="已读" width="100" />
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">查看</el-button>
            <el-button type="text">置顶</el-button>
            <el-button type="text" style="color:#f56c6c">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="oa-pagination" background layout="prev, pager, next" :total="50" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      keyword: '',
      type: '',
      list: [
        { title: '关于2026年端午节放假安排的通知', type: '公司公告', author: '行政部', publishTime: '2026-05-28 09:00', readCount: '86/86' },
        { title: '新版考勤管理制度', type: '制度规范', author: '人事部', publishTime: '2026-05-25 14:30', readCount: '72/86' },
        { title: '6月团建活动报名通知', type: '部门通知', author: '市场部', publishTime: '2026-06-01 10:00', readCount: '45/86' },
        { title: '信息系统安全使用规范', type: '制度规范', author: 'IT部', publishTime: '2026-06-02 16:00', readCount: '60/86' }
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
  background: linear-gradient(135deg, #ec4899, #f472b6);
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
