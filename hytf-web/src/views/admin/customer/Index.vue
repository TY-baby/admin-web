<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form :inline="true" :model="query" size="small">
        <el-form-item label="客户名称">
          <el-input v-model="query.keyword_name" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="抖音ID">
          <el-input v-model="query.keyword_douyin" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="添加时间">
          <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd"
                          start-placeholder="开始" end-placeholder="结束" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">查询</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">重置</el-button>
          <el-button type="success" icon="el-icon-plus" @click="openEdit()">新增客户</el-button>
          <el-button type="warning" icon="el-icon-download" @click="onExport">导出Excel</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading" row-key="id">
        <el-table-column type="expand">
          <template slot-scope="{ row }">
            <el-table :data="row.douyin_list" size="mini" border>
              <el-table-column prop="douyin_id" label="抖音号ID" />
              <el-table-column prop="douyin_name" label="名称" />
              <el-table-column prop="auto_code" label="6位码" width="80" />
              <el-table-column prop="nickname" label="昵称" />
              <el-table-column prop="recharge_amount" label="充值" width="90" />
              <el-table-column prop="balance" label="剩余" width="90" />
              <el-table-column prop="tier" label="档位" width="60" />
              <el-table-column label="授权" width="90">
                <template slot-scope="{ row: a }">{{ authLabel(a.auth_duration) }}</template>
              </el-table-column>
              <el-table-column label="到期时间" width="120">
                <template slot-scope="{ row: a }">{{ a.auth_end_at ? String(a.auth_end_at).slice(0,10) : '不限' }}</template>
              </el-table-column>
              <el-table-column label="状态" width="90">
                <template slot-scope="{ row: a }">
                  <el-tag size="mini" :type="statusTagType(a.status_label)">{{ a.status_label }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="80">
                <template slot-scope="{ row: a }">
                  <el-button size="mini" type="text" @click="openEdit(row, a)">编辑</el-button>
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-table-column>
        <el-table-column prop="customer_uid" label="客户UID" width="110" />
        <el-table-column prop="customer_name" label="客户名称" />
        <el-table-column prop="contact_name" label="联系人" width="100" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column label="抖音号数" width="90">
          <template slot-scope="{ row }">{{ (row.douyin_list || []).length }}</template>
        </el-table-column>
        <el-table-column label="总充值" width="100">
          <template slot-scope="{ row }">{{ (row.douyin_list||[]).reduce((s,a)=>s+Number(a.recharge_amount||0),0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="总剩余" width="100">
          <template slot-scope="{ row }">{{ (row.douyin_list||[]).reduce((s,a)=>s+Number(a.balance||0),0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="添加时间" width="160">
          <template slot-scope="{ row }">{{ String(row.created_at).replace('T',' ').slice(0,19) }}</template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="{ row }">
            <el-button size="mini" type="text" @click="openEdit(row)">编辑</el-button>
            <el-button size="mini" type="text" @click="openEdit(row, null, true)">追加抖音号</el-button>
            <el-button size="mini" type="text" style="color:#F56C6C" @click="onDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="mt-16" background layout="total, sizes, prev, pager, next, jumper"
                     :total="total" :current-page="query.page" :page-size="query.page_size"
                     :page-sizes="[10,20,50,100]"
                     @current-change="p => load(p)"
                     @size-change="s => { query.page_size = s; load(1) }" />
    </el-card>

    <edit-dialog ref="edit" @ok="load(query.page)" />
  </div>
</template>

<script>
import { listCustomers, deleteCustomer, exportUrl } from '@/api/adminCustomer'
import { getAdminToken } from '@/utils/auth'
import EditDialog from './EditDialog.vue'

export default {
  name: 'AdminCustomer',
  components: { EditDialog },
  data() {
    return {
      loading: false, rows: [], total: 0, dateRange: [],
      query: { keyword_name: '', keyword_douyin: '', page: 1, page_size: 20 }
    }
  },
  created() { this.load(1) },
  methods: {
    statusTagType(label) {
      if (label === '禁用') return 'info'
      if (label === '已到期') return 'danger'
      if (label === '即将到期') return 'warning'
      return 'success'
    },
    authLabel(v) {
      const m = { UNLIMITED: '不限', D3: '3天', D7: '7天', D30: '30天', CUSTOM: '自定义' }
      return m[v] || v || '-'
    },
    async load(page) {
      this.query.page = page || this.query.page
      const params = { ...this.query }
      if (this.dateRange && this.dateRange.length === 2) {
        params.date_from = this.dateRange[0]
        params.date_to = this.dateRange[1]
      }
      this.loading = true
      try {
        const { data } = await listCustomers(params)
        if (data.code === 0) { this.rows = data.data.items; this.total = data.data.total }
      } finally { this.loading = false }
    },
    reset() {
      this.query = { keyword_name: '', keyword_douyin: '', page: 1, page_size: 20 }
      this.dateRange = []
      this.load(1)
    },
    openEdit(row, acc, appendMode) { this.$refs.edit.open(row, acc, appendMode) },
    onDelete(row) {
      this.$confirm('确定删除客户【' + row.customer_name + '】及其所有抖音号数据吗?', '警告', { type: 'warning' })
        .then(async () => {
          const { data } = await deleteCustomer(row.id)
          if (data.code === 0) { this.$message.success('已删除'); this.load() }
        }).catch(() => {})
    },
    onExport() {
      const q = new URLSearchParams()
      if (this.query.keyword_name) q.append('keyword_name', this.query.keyword_name)
      if (this.query.keyword_douyin) q.append('keyword_douyin', this.query.keyword_douyin)
      if (this.dateRange && this.dateRange.length === 2) {
        q.append('date_from', this.dateRange[0])
        q.append('date_to', this.dateRange[1])
      }
      const url = exportUrl + '?' + q.toString()
      fetch(url, { headers: { Authorization: 'Bearer ' + getAdminToken() } })
        .then(r => r.blob()).then(b => {
          const a = document.createElement('a')
          a.href = URL.createObjectURL(b)
          a.download = this.exportFileName()
          a.click()
          URL.revokeObjectURL(a.href)
          this.$message.success('导出成功')
        }).catch(() => this.$message.error('导出失败'))
    },
    exportFileName() {
      const d = new Date()
      const pad = n => String(n).padStart(2, '0')
      const parts = []
      if (this.query.keyword_name) parts.push(this.query.keyword_name)
      if (this.query.keyword_douyin) parts.push(this.query.keyword_douyin)
      if (this.dateRange && this.dateRange.length === 2) {
        parts.push(this.dateRange[0] + '_' + this.dateRange[1])
      } else {
        parts.push(d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()))
      }
      return parts.join('_') + '.xlsx'
    }
  }
}
</script>