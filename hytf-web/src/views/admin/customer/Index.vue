<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form :inline="true" :model="query" size="small">
        <el-form-item label="瀹㈡埛鍚嶇О">
          <el-input v-model="query.keyword_name" placeholder="妯＄硦鎼滅储" clearable />
        </el-form-item>
        <el-form-item label="鎶栭煶ID">
          <el-input v-model="query.keyword_douyin" placeholder="妯＄硦鎼滅储" clearable />
        </el-form-item>
        <el-form-item label="娣诲姞鏃堕棿">
          <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd"
                          start-placeholder="寮€濮? end-placeholder="缁撴潫" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">鏌ヨ</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">閲嶇疆</el-button>
          <el-button type="success" icon="el-icon-plus" @click="openEdit()">鏂板瀹㈡埛</el-button>
          <el-button type="warning" icon="el-icon-download" @click="onExport">瀵煎嚭Excel</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading" row-key="id">
        <el-table-column type="expand">
          <template slot-scope="{ row }">
            <el-table :data="row.douyin_list" size="mini" border>
              <el-table-column prop="douyin_id" label="鎶栭煶鍙稩D" />
              <el-table-column prop="douyin_name" label="鍚嶇О" />
              <el-table-column prop="auto_code" label="6浣嶇爜" width="80" />
              <el-table-column prop="nickname" label="鏄电О" />
              <el-table-column prop="recharge_amount" label="鍏呭€? width="90" />
              <el-table-column prop="balance" label="鍓╀綑" width="90" />
              <el-table-column prop="tier" label="妗ｄ綅" width="60" />
              <el-table-column prop="auth_duration" label="鎺堟潈" width="90" />
              <el-table-column label="鍒版湡鏃堕棿" width="120">
                <template slot-scope="{ row: a }">{{ a.auth_end_at ? String(a.auth_end_at).slice(0,10) : '涓嶉檺' }}</template>
              </el-table-column>
              <el-table-column label="鐘舵€? width="90">
                <template slot-scope="{ row: a }">
                  <el-tag size="mini" :type="statusTagType(a.status_label)">{{ a.status_label }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="鎿嶄綔" width="80">
                <template slot-scope="{ row: a }">
                  <el-button size="mini" type="text" @click="openEdit(row, a)">缂栬緫</el-button>
                </template>
              </el-table-column>
            </el-table>
          </template>
        </el-table-column>
        <el-table-column prop="customer_uid" label="瀹㈡埛UID" width="110" />
        <el-table-column prop="customer_name" label="瀹㈡埛鍚嶇О" />
        <el-table-column prop="contact_name" label="鑱旂郴浜? width="100" />
        <el-table-column prop="phone" label="鎵嬫満鍙? width="120" />
        <el-table-column label="鎶栭煶鍙锋暟" width="90">
          <template slot-scope="{ row }">{{ (row.douyin_list || []).length }}</template>
        </el-table-column>
        <el-table-column label="鎬诲厖鍊? width="100">
          <template slot-scope="{ row }">{{ (row.douyin_list||[]).reduce((s,a)=>s+Number(a.recharge_amount||0),0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="鎬诲墿浣? width="100">
          <template slot-scope="{ row }">{{ (row.douyin_list||[]).reduce((s,a)=>s+Number(a.balance||0),0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="娣诲姞鏃堕棿" width="160">
          <template slot-scope="{ row }">{{ String(row.created_at).replace('T',' ').slice(0,19) }}</template>
        </el-table-column>
        <el-table-column prop="remark" label="澶囨敞" show-overflow-tooltip />
        <el-table-column label="鎿嶄綔" width="200" fixed="right">
          <template slot-scope="{ row }">
            <el-button size="mini" type="text" @click="openEdit(row)">缂栬緫</el-button>
            <el-button size="mini" type="text" @click="openEdit(row, null, true)">杩藉姞鎶栭煶鍙?/el-button>
            <el-button size="mini" type="text" style="color:#F56C6C" @click="onDelete(row)">鍒犻櫎</el-button>
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
      if (label === '绂佺敤') return 'info'
      if (label === '宸插埌鏈?) return 'danger'
      if (label === '鍗冲皢鍒版湡') return 'warning'
      return 'success'
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
      this.$confirm('纭畾鍒犻櫎瀹㈡埛銆? + row.customer_name + '銆戝強鍏舵墍鏈夋姈闊冲彿鏁版嵁锛?, '璀﹀憡', { type: 'warning' })
        .then(async () => {
          const { data } = await deleteCustomer(row.id)
          if (data.code === 0) { this.$message.success('宸插垹闄?); this.load() }
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
          a.download = 'customers_' + Date.now() + '.xlsx'
          a.click()
          URL.revokeObjectURL(a.href)
          this.$message.success('瀵煎嚭鎴愬姛')
        }).catch(() => this.$message.error('瀵煎嚭澶辫触'))
    }
  }
}
</script>