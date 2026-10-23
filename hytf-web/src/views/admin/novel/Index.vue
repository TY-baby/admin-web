<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form inline size="small">
        <el-form-item label="客户名称">
          <el-select v-model="query.keyword_name" filterable remote clearable placeholder="输入客户名称搜索"
                     :remote-method="searchCustomer" :loading="custLoading" style="width:200px">
            <el-option v-for="c in custOptions" :key="c.id" :label="c.customer_name" :value="c.customer_name" />
          </el-select>
        </el-form-item>
        <el-form-item label="添加时间">
          <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd"
                          start-placeholder="开始" end-placeholder="结束" />
        </el-form-item>
        <el-form-item label="投放时间">
          <el-date-picker v-model="launchRange" type="daterange" value-format="yyyy-MM-dd"
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
      <el-alert type="info" :closable="false" show-icon class="mb-16"
                title="本网页为网文投放只读统计视图；新增客户/追加金额/追加平台/删除请统一在【用户管理】操作" />
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column prop="customer_uid" label="客户UID" width="110" />
        <el-table-column prop="customer_name" label="客户名称" min-width="120" />
        <el-table-column prop="contact_name" label="联系人" width="100" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column prop="url_count" label="网址数" width="80" align="center" />
        <el-table-column label="总充值" width="100" align="right">
          <template slot-scope="{ row }">{{ Number(row.total_recharge || 0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="总剩余" width="100" align="right">
          <template slot-scope="{ row }">{{ Number(row.total_balance || 0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="添加时间" width="160">
          <template slot-scope="{ row }">{{ fmt(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="投放时间" width="160">
          <template slot-scope="{ row }">{{ fmt(row.launch_at) }}</template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="120" show-overflow-tooltip />
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
import { listNovel, novelExportUrl } from '@/api/adminNovel'
import { getAdminToken } from '@/utils/auth'

export default {
  name: 'AdminNovel',
  data() {
    return {
      loading: false, rows: [], total: 0,
      dateRange: [], launchRange: [],
      query: { keyword_name: '', page: 1, page_size: 20 },
      custOptions: [], custLoading: false
    }
  },
  created() { this.load(1) },
  methods: {
    fmt(t) { return t ? String(t).replace('T', ' ').slice(0, 19) : '-' },
    async searchCustomer(kw) {
      this.custLoading = true
      try {
        const { data } = await listNovel({ keyword_name: kw || '', page: 1, page_size: 20 })
        if (data.code === 0) this.custOptions = data.data.items || []
      } finally { this.custLoading = false }
    },
    buildParams() {
      const p = { ...this.query }
      if (this.dateRange && this.dateRange.length === 2) { p.date_from = this.dateRange[0]; p.date_to = this.dateRange[1] }
      if (this.launchRange && this.launchRange.length === 2) { p.launch_from = this.launchRange[0]; p.launch_to = this.launchRange[1] }
      return p
    },
    async load(page) {
      this.query.page = page || this.query.page
      this.loading = true
      try {
        const { data } = await listNovel(this.buildParams())
        if (data.code === 0) { this.rows = data.data.items; this.total = data.data.total }
      } finally { this.loading = false }
    },
    reset() {
      this.query = { keyword_name: '', page: 1, page_size: 20 }
      this.dateRange = []; this.launchRange = []
      this.load(1)
    },
    onExport() {
      const p = this.buildParams()
      if (!p.keyword_name && !p.date_from && !p.launch_from) {
        this.$message.warning('请先输入查询条件（客户名称/添加时间/投放时间）再导出'); return
      }
      const q = new URLSearchParams()
      q.append('launch_type', 'NOVEL_PROMO')
      q.append('promo_only', '1')
      if (p.keyword_name) q.append('keyword_name', p.keyword_name)
      if (p.date_from) q.append('date_from', p.date_from)
      if (p.date_to) q.append('date_to', p.date_to)
      if (p.launch_from) q.append('launch_from', p.launch_from)
      if (p.launch_to) q.append('launch_to', p.launch_to)
      fetch(novelExportUrl + '?' + q.toString(), { headers: { Authorization: 'Bearer ' + getAdminToken() } })
        .then(async r => {
          const ct = r.headers.get('content-type') || ''
          if (ct.indexOf('json') !== 1 && ct.indexOf('json') !== -1) { return r.blob() }
          if (ct.indexOf('json') !== -1) { const j = await r.json(); this.$message.error(j.msg || '导出失败'); return null }
          return r.blob()
        })
        .then(b => {
          if (!b) return
          const a = document.createElement('a')
          a.href = URL.createObjectURL(b)
          a.download = `网文客户_${new Date().toISOString().slice(0, 10)}.xlsx`
          a.click(); URL.revokeObjectURL(a.href)
          this.$message.success('导出成功')
        }).catch(() => this.$message.error('导出失败'))
    }
  }
}
</script>