<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">车辆管理</div>
      <div class="oa-desc">公车档案、用车申请与车辆调度</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-input v-model="keyword" placeholder="车牌号/车辆型号" clearable style="width:260px" />
        <el-select v-model="status" placeholder="车辆状态" clearable style="width:140px">
          <el-option label="可用" value="available" />
          <el-option label="使用中" value="using" />
          <el-option label="维修中" value="repair" />
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增车辆</el-button>
        <el-button type="warning" icon="el-icon-position">用车申请</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="plate" label="车牌号" width="120" />
        <el-table-column prop="model" label="车辆型号" />
        <el-table-column prop="driver" label="当前司机" width="120" />
        <el-table-column prop="department" label="所属部门" width="140" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.statusType">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template>
            <el-button type="text">详情</el-button>
            <el-button type="text">调度</el-button>
            <el-button type="text">维保</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="oa-pagination" background layout="prev, pager, next" :total="30" />
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
        { plate: '京A·12345', model: '别克GL8', driver: '刘师傅', department: '行政部', status: '使用中', statusType: 'warning' },
        { plate: '京A·67890', model: '大众帕萨特', driver: '—', department: '行政部', status: '可用', statusType: 'success' },
        { plate: '京B·11111', model: '丰田考斯特', driver: '张师傅', department: '市场部', status: '维修中', statusType: 'danger' },
        { plate: '京B·22222', model: '哈弗H6', driver: '—', department: '生产部', status: '可用', statusType: 'success' }
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
  background: linear-gradient(135deg, #3b82f6, #60a5fa);
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
