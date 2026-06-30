<template>
  <div class="erp-page">
    <div class="erp-header">
      <div class="erp-title">仓库管理</div>
      <div class="erp-desc">仓库档案、库位与出入库记录</div>
    </div>

    <div class="erp-card">
      <div class="erp-toolbar">
        <el-input v-model="keyword" placeholder="仓库名称" clearable style="width:260px" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增仓库</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="code" label="仓库编码" width="120" />
        <el-table-column prop="name" label="仓库名称" />
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="manager" label="负责人" width="120" />
        <el-table-column prop="capacity" label="容量(m²)" width="120" />
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">库位</el-button>
            <el-button type="text">编辑</el-button>
            <el-button type="text">记录</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="erp-pagination" background layout="prev, pager, next" :total="50" />
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
        { code: 'WH01', name: 'A1原料仓', address: '厂区东侧1号库', manager: '刘强', capacity: 3000 },
        { code: 'WH02', name: 'B2半成品仓', address: '厂区中部2号库', manager: '陈芳', capacity: 2000 },
        { code: 'WH03', name: 'C1成品仓', address: '厂区西侧3号库', manager: '赵敏', capacity: 2500 },
        { code: 'WH04', name: 'D1备品备件仓', address: '厂区北侧4号库', manager: '孙伟', capacity: 1200 }
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
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
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
