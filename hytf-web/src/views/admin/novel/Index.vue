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
          <el-button type="success" icon="el-icon-plus" @click="openCreate">新增客户</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
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
        <el-table-column label="操作" width="150" fixed="right">
          <template slot-scope="{ row }">
            <el-button type="text" size="mini" @click="openRecharge(row)">追加金额</el-button>
            <el-button type="text" size="mini" style="color:#F56C6C" @click="onDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="mt-16" background layout="total, sizes, prev, pager, next, jumper"
                     :total="total" :current-page="query.page" :page-size="query.page_size"
                     :page-sizes="[10,20,50,100]"
                     @current-change="p => load(p)"
                     @size-change="s => { query.page_size = s; load(1) }" />
    </el-card>

    <el-dialog title="新增网文客户" :visible.sync="createVisible" width="460px" :close-on-click-modal="false">
      <el-form ref="createForm" :model="createForm" :rules="createRules" label-width="90px" size="small">
        <el-form-item label="客户名称" prop="customer_name">
          <el-input v-model="createForm.customer_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="createForm.contact_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="createForm.phone" maxlength="11" placeholder="A端登录账号,默认密码=手机号+123" />
        </el-form-item>
        <el-form-item label="充值金额" prop="recharge_amount">
          <el-input v-model="createForm.recharge_amount" placeholder="正整数,单位元" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="createForm.remark" type="textarea" :rows="2" maxlength="255" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button size="small" @click="createVisible=false">取消</el-button>
        <el-button size="small" type="primary" :loading="saving" @click="submitCreate">保存</el-button>
      </div>
    </el-dialog>

    <el-dialog title="追加金额" :visible.sync="rechargeVisible" width="400px" :close-on-click-modal="false">
      <el-form label-width="90px" size="small">
        <el-form-item label="客户名称"><span>{{ rechargeRow && rechargeRow.customer_name }}</span></el-form-item>
        <el-form-item label="当前剩余"><span>￥{{ Number((rechargeRow && rechargeRow.total_balance) || 0).toFixed(2) }}</span></el-form-item>
        <el-form-item label="追加金额" required>
          <el-input v-model="rechargeAmount" placeholder="正整数,单位元(累加)" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button size="small" @click="rechargeVisible=false">取消</el-button>
        <el-button size="small" type="primary" :loading="saving" @click="submitRecharge">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listNovel, createNovelCustomer, novelExportUrl } from '@/api/adminNovel'
import { listCustomers, updateDouyin, deleteCustomer } from '@/api/adminCustomer'
import { getAdminToken } from '@/utils/auth'
import { isPhone, isPositiveInt } from '@/utils/validate'

export default {
  name: 'AdminNovel',
  data() {
    return {
      loading: false, saving: false, rows: [], total: 0,
      dateRange: [], launchRange: [],
      query: { keyword_name: '', page: 1, page_size: 20 },
      custOptions: [], custLoading: false,
      createVisible: false,
      createForm: { customer_name: '', contact_name: '', phone: '', recharge_amount: '', remark: '' },
      createRules: {
        customer_name: [{ required: true, message: '请输入客户名称', trigger: 'blur' }],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { validator: (r, v, cb) => isPhone(v) ? cb() : cb(new Error('手机号格式不正确')), trigger: 'blur' }
        ],
        recharge_amount: [
          { required: true, message: '请输入充值金额', trigger: 'blur' },
          { validator: (r, v, cb) => isPositiveInt(v) ? cb() : cb(new Error('请输入正整数')), trigger: 'blur' }
        ]
      },
      rechargeVisible: false, rechargeRow: null, rechargeAmount: ''
    }
  },
  created() { this.load(1) },
  methods: {
    fmt(t) { return t ? String(t).replace('T', ' ').slice(0, 19) : '-' },
    async searchCustomer(kw) {
      this.custLoading = true
      try {
        const { data } = await listCustomers({ keyword_name: kw, page: 1, page_size: 20 })
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
    openCreate() {
      this.createForm = { customer_name: '', contact_name: '', phone: '', recharge_amount: '', remark: '' }
      this.createVisible = true
      this.$nextTick(() => this.$refs.createForm && this.$refs.createForm.clearValidate())
    },
    submitCreate() {
      this.$refs.createForm.validate(async ok => {
        if (!ok) return
        this.saving = true
        try {
          const { data } = await createNovelCustomer({
            customer_name: this.createForm.customer_name,
            contact_name: this.createForm.contact_name,
            phone: this.createForm.phone,
            recharge_amount: Number(this.createForm.recharge_amount),
            remark: this.createForm.remark
          })
          if (data.code === 0) { this.$message.success('新增成功'); this.createVisible = false; this.load(1) }
          else this.$message.error(data.msg || '新增失败')
        } finally { this.saving = false }
      })
    },
    openRecharge(row) {
      if (!row.promo_account_id) { this.$message.warning('该客户暂无可追加的网文推广账户'); return }
      this.rechargeRow = row; this.rechargeAmount = ''; this.rechargeVisible = true
    },
    async submitRecharge() {
      if (!isPositiveInt(this.rechargeAmount)) { this.$message.warning('请输入正整数金额'); return }
      this.saving = true
      try {
        const { data } = await updateDouyin(this.rechargeRow.promo_account_id, { recharge_amount: Number(this.rechargeAmount) })
        if (data.code === 0) { this.$message.success('追加成功'); this.rechargeVisible = false; this.load(this.query.page) }
        else this.$message.error(data.msg || '追加失败')
      } finally { this.saving = false }
    },
    onDelete(row) {
      this.$confirm(`确认删除客户【${row.customer_name}】及其全部数据？`, '提示', { type: 'warning' })
        .then(async () => {
          const { data } = await deleteCustomer(row.id)
          if (data.code === 0) { this.$message.success('删除成功'); this.load(1) }
          else this.$message.error(data.msg || '删除失败')
        }).catch(() => {})
    },
    onExport() {
      const p = this.buildParams()
      if (!p.keyword_name && !p.date_from && !p.launch_from) {
        this.$message.warning('请先输入查询条件（客户名称/添加时间/投放时间）再导出'); return
      }
      const q = new URLSearchParams()
      q.append('launch_type', 'NOVEL_PROMO')
      if (p.keyword_name) q.append('keyword_name', p.keyword_name)
      if (p.date_from) q.append('date_from', p.date_from)
      if (p.date_to) q.append('date_to', p.date_to)
      if (p.launch_from) q.append('launch_from', p.launch_from)
      if (p.launch_to) q.append('launch_to', p.launch_to)
      fetch(novelExportUrl + '?' + q.toString(), { headers: { Authorization: 'Bearer ' + getAdminToken() } })
        .then(async r => {
          const ct = r.headers.get('content-type') || ''
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