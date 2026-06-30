<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">文档中心</div>
      <div class="oa-desc">企业文档、知识库与文件共享</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-input v-model="keyword" placeholder="文档名称" clearable style="width:260px" />
        <el-select v-model="type" placeholder="文档类型" clearable style="width:140px">
          <el-option label="制度文档" value="policy" />
          <el-option label="项目文档" value="project" />
          <el-option label="培训资料" value="training" />
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-upload2">上传文档</el-button>
        <el-button type="warning" icon="el-icon-folder-add">新建文件夹</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="name" label="文档名称" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="size" label="大小" width="100" />
        <el-table-column prop="author" label="上传人" width="120" />
        <el-table-column prop="updateTime" label="更新时间" width="160" />
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">预览</el-button>
            <el-button type="text">下载</el-button>
            <el-button type="text" style="color:#f56c6c">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="oa-pagination" background layout="prev, pager, next" :total="80" />
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
        { name: '2026年员工手册.pdf', type: '制度文档', size: '2.4MB', author: '人事部', updateTime: '2026-05-25 14:30' },
        { name: 'OA系统使用培训.pptx', type: '培训资料', size: '8.6MB', author: 'IT部', updateTime: '2026-06-01 10:00' },
        { name: '6月销售计划.xlsx', type: '项目文档', size: '1.2MB', author: '销售部', updateTime: '2026-06-02 09:00' },
        { name: '产品需求说明书.docx', type: '项目文档', size: '3.5MB', author: '产品部', updateTime: '2026-06-03 16:30' }
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
  background: linear-gradient(135deg, #6366f1, #818cf8);
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
