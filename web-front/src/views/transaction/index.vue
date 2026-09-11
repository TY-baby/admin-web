<template>
  <div class="transaction-page">
    <!-- ===== 统计卡片 ===== -->
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-ico blue"><i class="el-icon-document"></i></div>
        <div class="stat-body">
          <div class="stat-value">{{ total }}</div>
          <div class="stat-label">新闻条目</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-ico cyan"><i class="el-icon-pointer"></i></div>
        <div class="stat-body">
          <div class="stat-value">{{ summary.total_click }}</div>
          <div class="stat-label">总点击次数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-ico orange"><i class="el-icon-coin"></i></div>
        <div class="stat-body">
          <div class="stat-value">{{ summary.total_fee }}</div>
          <div class="stat-label">总费用（元）</div>
        </div>
      </div>
    </div>

    <!-- ===== 查询区 ===== -->
    <el-card shadow="never" class="filter-card">
      <el-form :inline="true" size="small" @submit.native.prevent>
        <el-form-item label="新闻标题">
          <el-input v-model="query.keyword" placeholder="请输入新闻标题关键字" clearable
                    style="width: 260px" @keyup.enter.native="search" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="search">查询</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- ===== 数据表格 ===== -->
    <el-card shadow="never" class="table-card">
      <div slot="header" class="card-header">
        <span class="card-title"><i class="el-icon-s-data"></i> 交易信息</span>
        <el-button type="text" icon="el-icon-refresh" @click="load">刷新</el-button>
      </div>

      <el-table :data="list" v-loading="loading" border stripe style="width: 100%">
        <el-table-column type="index" label="序号" width="70" align="center" />
        <el-table-column prop="title" label="新闻标题" min-width="260" show-overflow-tooltip />
        <el-table-column prop="click_count" label="点击次数" width="120" align="center" sortable>
          <template slot-scope="scope">
            <el-tag size="small" type="primary" effect="plain">{{ scope.row.click_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="click_time" label="点击时间" width="190" align="center" />
        <el-table-column prop="ip" label="IP" width="160" align="center" />
        <el-table-column prop="fee" label="费用（元）" width="130" align="center">
          <template slot-scope="scope">
            <span class="fee">{{ Number(scope.row.fee).toFixed(2) }}</span>
          </template>
        </el-table-column>
        <template slot="empty">
          <div class="empty-box">
            <i class="el-icon-folder-opened"></i>
            <p>暂无点击数据，去官网点几条新闻试试吧</p>
          </div>
        </template>
      </el-table>

      <el-pagination
        :current-page.sync="query.page"
        :page-size="query.size"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="load"
        @current-change="load" />
    </el-card>
  </div>
</template>

<script>
import { getTransactions } from '@/api/transaction'

export default {
  name: 'TransactionPage',
  data() {
    return {
      loading: false,
      list: [],
      total: 0,
      summary: { total_click: 0, total_fee: 0 },
      query: { keyword: '', page: 1, size: 10 }
    }
  },
  created() {
    this.load()
  },
  methods: {
    async load() {
      this.loading = true
      try {
        const res = await getTransactions(this.query)
        this.list = res.list || []
        this.total = res.total || 0
        this.summary = res.summary || { total_click: 0, total_fee: 0 }
      } catch (e) {
        this.list = []
        this.total = 0
      } finally {
        this.loading = false
      }
    },
    search() {
      this.query.page = 1
      this.load()
    },
    reset() {
      this.query = { keyword: '', page: 1, size: 10 }
      this.load()
    }
  }
}
</script>

<style lang="scss" scoped>
.stat-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 16px; }
.stat-card {
  display: flex; align-items: center; gap: 16px;
  background: #fff; border-radius: 12px; padding: 20px 22px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  transition: all .25s;
  &:hover { transform: translateY(-3px); box-shadow: 0 10px 26px rgba(15,23,42,.09); }
}
.stat-ico {
  width: 48px; height: 48px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; color: #fff; flex-shrink: 0;
  &.blue   { background: linear-gradient(135deg, #3b82f6, #6366f1); }
  &.cyan   { background: linear-gradient(135deg, #06b6d4, #0ea5e9); }
  &.orange { background: linear-gradient(135deg, #f59e0b, #f97316); }
}
.stat-value { font-size: 26px; font-weight: 800; color: #0f172a; line-height: 1.2; }
.stat-label { font-size: 13px; color: #94a3b8; margin-top: 4px; }

.filter-card { margin-bottom: 16px; }
.filter-card ::v-deep .el-card__body { padding: 18px 20px 0; }
.filter-card ::v-deep .el-form-item { margin-bottom: 18px; }

.card-header { display: flex; align-items: center; justify-content: space-between; }
.card-title { font-size: 15px; font-weight: 600; color: #1e293b; i { color: #0ea5e9; margin-right: 6px; } }

.fee { color: #f59e0b; font-weight: 700; }

.empty-box {
  padding: 46px 0; color: #94a3b8;
  i { font-size: 46px; color: #cbd5e1; display: block; margin-bottom: 12px; }
  p { font-size: 13px; }
}

@media (max-width: 900px) {
  .stat-row { grid-template-columns: 1fr; }
}
</style>