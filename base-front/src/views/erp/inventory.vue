<template>
  <div class="erp-page">
    <div class="erp-header">
      <div class="erp-title">库存管理</div>
      <div class="erp-desc">实时库存、库存预警与盘点</div>
    </div>

    <div class="erp-card">
      <div class="erp-toolbar">
        <el-input v-model="keyword" placeholder="物料编码/名称" clearable style="width:260px" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="warning" icon="el-icon-refresh">库存盘点</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="code" label="物料编码" width="140" />
        <el-table-column prop="name" label="物料名称" />
        <el-table-column prop="category" label="分类" width="120" />
        <el-table-column prop="quantity" label="库存数量" width="120" />
        <el-table-column prop="safe" label="安全库存" width="120" />
        <el-table-column prop="warehouse" label="所在仓库" width="140" />
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">出入库</el-button>
            <el-button type="text">调拨</el-button>
            <el-button type="text">明细</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="erp-pagination" background layout="prev, pager, next" :total="120" />
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
        { code: 'M1001', name: '碳钢板材 2mm', category: '原材料', quantity: 5200, safe: 1000, warehouse: 'A1原料仓' },
        { code: 'M1002', name: '不锈钢管材', category: '原材料', quantity: 1800, safe: 500, warehouse: 'A1原料仓' },
        { code: 'P2001', name: '工业控制模块', category: '半成品', quantity: 320, safe: 200, warehouse: 'B2半成品仓' },
        { code: 'F3001', name: '智能温控设备', category: '成品', quantity: 86, safe: 50, warehouse: 'C1成品仓' }
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
  background: linear-gradient(135deg, #10b981, #34d399);
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
