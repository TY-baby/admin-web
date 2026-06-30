<template>
  <div class="erp-page">
    <div class="erp-header">
      <div class="erp-title">供应商管理</div>
      <div class="erp-desc">供应商档案、评级与合作记录</div>
    </div>

    <div class="erp-card">
      <div class="erp-toolbar">
        <el-input v-model="keyword" placeholder="供应商名称" clearable style="width:260px" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增供应商</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="name" label="供应商名称" />
        <el-table-column prop="contact" label="联系人" width="120" />
        <el-table-column prop="phone" label="联系电话" width="140" />
        <el-table-column prop="level" label="等级" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.level === 'A' ? 'success' : scope.row.level === 'B' ? 'warning' : 'info'">{{ scope.row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="cooperation" label="合作次数" width="100" />
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">详情</el-button>
            <el-button type="text">编辑</el-button>
            <el-button type="text" style="color:#f56c6c">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="erp-pagination" background layout="prev, pager, next" :total="80" />
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
        { name: '华东钢铁有限公司', contact: '张经理', phone: '13800138000', level: 'A', cooperation: 32 },
        { name: '南方电子元器件厂', contact: '李工', phone: '13900139000', level: 'A', cooperation: 28 },
        { name: '环球物流包装', contact: '王小姐', phone: '13700137000', level: 'B', cooperation: 15 },
        { name: '精密机械加工厂', contact: '赵总', phone: '13600136000', level: 'C', cooperation: 6 }
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
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
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
