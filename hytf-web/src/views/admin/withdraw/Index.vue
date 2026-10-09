<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form :inline="true" :model="query" size="small">
        <el-form-item label="客户名称">
          <el-input v-model="query.keyword_name" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="query.keyword_phone" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="添加时间">
          <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd"
                          start-placeholder="开始" end-placeholder="结束" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">查询</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">重置</el-button>
          <el-button type="warning" icon="el-icon-download" @click="onExport">导出Excel</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column prop="customer_uid" label="客户UID" width="110" />
        <el-table-column prop="customer_name" label="客户名称" />
        <el-table-column prop="contact_name" label="联系人" width="100" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column prop="pay_date" label="打款日期" width="130" />
        <el-table-column prop="id_count" label="产出ID数量" width="120" />
        <el-table-column label="总充值金额(元)" width="140">
          <template slot-scope="{ row }">{{ Number(row.total_recharge || 0).toFixed(2) }}</template>
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
import { listWithdraws, withdrawExportUrl } from '@/api/adminWithdraw'
import { getAdminToken } from '@/utils/auth'

export default {
  name: 'AdminWithdraw',
  data() {
    return {
      loading: false, rows: [], total: 0, dateRange: [],
      query: { keyword_name: '', keyword_phone: '', page: 1, page_size: 20 }
    }
  },
  created() { this.load(1) },
  methods: {
    buildParams() {
      const params = { ...this.query }
      if (this.dateRange && this.dateRange.length === 2) {
        params.date_from = this.dateRange[0]
        params.date_to = this.dateRange[1]
      }
      return params
    },
    async load(page) {
      this.query.page = page || this.query.page
      this.loading = true
      try {
        const { data } = await listWithdraws(this.buildParams())
        if (data.code === 0) { this.rows = data.data.items; this.total = data.data.total }
      } finally { this.loading = false }
    },
    reset() {
      this.query = { keyword_name: '', keyword_phone: '', page: 1, page_size: 20 }
      this.dateRange = []
      this.load(1)
    },
    hasCond() {
      return this.query.keyword_name || this.query.keyword_phone ||
             (this.dateRange && this.dateRange.length === 2)
    },
    onExport() {
      if (!this.hasCond()) { this.$message.warning('必须先输入查询条件进行导出'); return }
      const p = this.buildParams()
      const q = new URLSearchParams()
      if (p.keyword_name) q.append('keyword_name', p.keyword_name)
      if (p.keyword_phone) q.append('keyword_phone', p.keyword_phone)
      if (p.date_from) q.append('date_from', p.date_from)
      if (p.date_to) q.append('date_to', p.date_to)
      fetch(withdrawExportUrl + '?' + q.toString(), { headers: { Authorization: 'Bearer ' + getAdminToken() } })
        .then(r => r.blob()).then(b => {
          const a = document.createElement('a')
          a.href = URL.createObjectURL(b)
          a.download = '出款管理_' + new Date().getTime() + '.xlsx'
          a.click()
          URL.revokeObjectURL(a.href)
          this.$message.success('导出成功')
        }).catch(() => this.$message.error('导出失败'))
    }
  }
}
</script>