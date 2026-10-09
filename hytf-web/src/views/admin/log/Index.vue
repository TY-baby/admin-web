<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form :inline="true" :model="query" size="small">
        <el-form-item label="账号">
          <el-input v-model="query.keyword_username" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="时间">
          <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd"
                          start-placeholder="开始" end-placeholder="结束" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">查询</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column prop="username" label="账号" width="120" />
        <el-table-column prop="action" label="行为" width="90" />
        <el-table-column prop="method" label="方法" width="80" />
        <el-table-column prop="path" label="访问路径" show-overflow-tooltip />
        <el-table-column prop="ip" label="IP" width="140" />
        <el-table-column label="时间" width="170">
          <template slot-scope="{ row }">{{ row.created_at ? String(row.created_at).replace('T',' ').slice(0,19) : '-' }}</template>
        </el-table-column>
      </el-table>
      <el-pagination class="mt-16" background layout="total, sizes, prev, pager, next, jumper"
                     :total="total" :current-page="query.page" :page-size="query.page_size"
                     :page-sizes="[10,20,50,100]"
                     @current-change="p => load(p)"
                     @size-change="s => { query.page_size = s; load(1) }" />
    </el-card>
  </div>
</template>

<script>
import { listLogs } from '@/api/adminSystem'
export default {
  name: 'AdminLog',
  data() {
    return {
      loading: false, rows: [], total: 0, dateRange: [],
      query: { keyword_username: '', page: 1, page_size: 20 }
    }
  },
  created() { this.load(1) },
  methods: {
    async load(page) {
      this.query.page = page || this.query.page
      const params = { ...this.query }
      if (this.dateRange && this.dateRange.length === 2) {
        params.date_from = this.dateRange[0]
        params.date_to = this.dateRange[1]
      }
      this.loading = true
      try {
        const { data } = await listLogs(params)
        if (data.code === 0) { this.rows = data.data.items; this.total = data.data.total }
      } finally { this.loading = false }
    },
    reset() {
      this.query = { keyword_username: '', page: 1, page_size: 20 }
      this.dateRange = []
      this.load(1)
    }
  }
}
</script>