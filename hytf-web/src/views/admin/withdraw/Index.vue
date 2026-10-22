<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form :inline="true" :model="query" size="small">
        <el-form-item label="关键词">
          <el-input v-model="query.keyword" placeholder="打款对象/卡号/客户/投放ID 模糊匹配" clearable style="width:260px" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="query.launch_type" placeholder="全部" clearable style="width:140px">
            <el-option label="首充" value="FIRST_CHARGE" />
            <el-option label="直播曝光度" value="EXPOSURE" />
            <el-option label="网文推广" value="NOVEL_PROMO" />
          </el-select>
        </el-form-item>
        <el-form-item label="创建时间">
          <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd"
                          start-placeholder="开始" end-placeholder="结束" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">查询</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">重置</el-button>
          <el-button type="success" icon="el-icon-plus" @click="openDialog">新增出款</el-button>
          <el-button type="warning" icon="el-icon-download" @click="onExport">导出Excel</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column prop="payee_holder_name" label="打款对象" width="110" />
        <el-table-column prop="payee_card_no" label="卡号" width="200" />
        <el-table-column prop="customer_name" label="客户名称" width="120" />
        <el-table-column prop="platform_name" label="平台" width="100" />
        <el-table-column prop="douyin_id" label="投放ID" width="130" />
        <el-table-column label="类型" width="110">
          <template slot-scope="{ row }">
            <el-tag size="mini" :type="row.launch_type === 'EXPOSURE' ? 'warning' : 'success'">
              {{ row.launch_type_label || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="结算条数/热度" width="130" align="center">
          <template slot-scope="{ row }">
            <span v-if="row.launch_type === 'EXPOSURE'">{{ row.heat_value || 0 }} 热度</span>
            <span v-else>{{ row.generated_count || 0 }} 条</span>
          </template>
        </el-table-column>
        <el-table-column label="结算金额(元)" width="120" align="right">
          <template slot-scope="{ row }">{{ Number(row.payable_amount || 0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column prop="settle_date" label="结算日期" width="120" />
        <el-table-column prop="operator" label="操作人" width="90" />
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="80">
          <template slot-scope="{ row }">
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

    <el-dialog title="新增出款" :visible.sync="dialogVisible" width="600px"
               :close-on-click-modal="false" @open="onDialogOpen">
      <el-form :model="form" label-width="110px" size="small">
        <el-form-item label="打款对象" required>
          <el-select v-model="form.payee_id" placeholder="请选择打款对象" style="width:100%">
            <el-option v-for="p in payees" :key="p.id" :label="p.display_name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="selectedPayee" label="开户行">
          <span>{{ selectedPayee.bank_name }}</span>
        </el-form-item>
        <el-form-item v-if="selectedPayee" label="卡号">
          <span>{{ selectedPayee.card_no }}</span>
        </el-form-item>
        <el-form-item label="类型" required>
          <el-select v-model="form.launch_type" placeholder="请先选择类型" style="width:100%" @change="onTypeChange">
            <el-option label="首充" value="FIRST_CHARGE" />
            <el-option label="直播曝光度" value="EXPOSURE" />
            <el-option label="网文推广" value="NOVEL_PROMO" />
          </el-select>
        </el-form-item>
        <el-form-item :label="form.launch_type === 'NOVEL_PROMO' ? '客户/平台/内容' : '客户/平台/ID'" required>
          <el-cascader v-model="form.cascade"
                       :options="form.launch_type === 'NOVEL_PROMO' ? novelOptions : customerOptions"
                       :props="cascaderProps" :disabled="!form.launch_type"
                       :placeholder="form.launch_type ? '请选择' : '请先选择类型'"
                       style="width:100%" filterable clearable @change="onCascadeChange" />
        </el-form-item>
        <el-form-item v-if="form.launch_type === 'FIRST_CHARGE' || form.launch_type === 'NOVEL_PROMO'" label="生成条数">
          <el-input-number v-model="form.generated_count" :min="0" :step="1" style="width:200px" />
          <span style="margin-left:8px;color:#909399">条（剩余可出款，默认带出，可下调）</span>
        </el-form-item>
        <el-form-item v-if="form.launch_type === 'EXPOSURE'" label="热度">
          <el-input-number v-model="form.heat_value" :min="0" :step="1" style="width:200px" />
          <span style="margin-left:8px;color:#909399">剩余可出款热度，默认带出，可下调</span>
        </el-form-item>
        <el-form-item label="结算金额" required>
          <el-input v-model="form.payable_amount" placeholder="手动输入,单位元" style="width:200px">
            <template slot="append">元</template>
          </el-input>
        </el-form-item>
        <el-form-item label="结算日期" required>
          <el-date-picker v-model="form.settle_date" type="date" value-format="yyyy-MM-dd"
                          placeholder="选择结算日期" style="width:200px" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" maxlength="255" show-word-limit />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button size="small" @click="dialogVisible=false">取 消</el-button>
        <el-button size="small" type="primary" :loading="submitting" @click="onSubmit">提 交</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listWithdraws, listPayees, listWithdrawCustomers, previewWithdraw,
         previewNovelWithdraw, createWithdraw, deleteWithdraw, withdrawExportUrl } from '@/api/adminWithdraw'
import { getAdminToken } from '@/utils/auth'

export default {
  name: 'AdminWithdraw',
  data() {
    const d = new Date()
    const today = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0')
    return {
      loading: false, rows: [], total: 0, dateRange: [],
      query: { keyword: '', launch_type: '', page: 1, page_size: 20 },
      dialogVisible: false, submitting: false,
      payees: [], customerOptions: [], novelOptions: [],
      form: {
        payee_id: null, cascade: [], launch_type: '',
        generated_count: 0, heat_value: 0,
        customer_id: null, platform_code: '', promo_content: '',
        payable_amount: '', settle_date: today, remark: ''
      },
      cascaderProps: { value: 'value', label: 'label', children: 'children' }
    }
  },
  computed: {
    selectedPayee() { return this.payees.find(p => p.id === this.form.payee_id) || null }
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
      this.query = { keyword: '', launch_type: '', page: 1, page_size: 20 }
      this.dateRange = []
      this.load(1)
    },
    openDialog() { this.dialogVisible = true },
    async onDialogOpen() {
      const d = new Date()
      const today = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0')
      this.form = { payee_id: null, cascade: [], launch_type: '',
                    generated_count: 0, heat_value: 0,
                    customer_id: null, platform_code: '', promo_content: '',
                    payable_amount: '', settle_date: today, remark: '' }
      try {
        const [pRes, cRes] = await Promise.all([listPayees(), listWithdrawCustomers()])
        if (pRes.data.code === 0) this.payees = pRes.data.data || []
        if (cRes.data.code === 0) {
          const list = cRes.data.data || []
          // 首充/曝光：客户 → 平台 → ID
          this.customerOptions = list.map(c => {
            const byPlat = {}
            ;(c.accounts || []).forEach(a => {
              if (!byPlat[a.platform_code]) {
                byPlat[a.platform_code] = { value: 'p_' + a.platform_code, label: a.platform_name || a.platform_code, children: [] }
              }
              byPlat[a.platform_code].children.push({
                value: 'a_' + a.id,
                label: a.douyin_id + (a.douyin_name ? '（' + a.douyin_name + '）' : ''),
                isLeaf: true, accountId: a.id
              })
            })
            return { value: 'c_' + c.id, label: c.customer_name, children: Object.values(byPlat) }
          })
          // 网文推广：客户 → 平台 → 内容
          this.novelOptions = list.map(c => ({
            value: 'c_' + c.id, label: c.customer_name, customerId: c.id,
            children: (c.novel_options || []).map(p => ({
              value: 'p_' + p.platform_code, label: p.platform_name,
              customerId: c.id, platformCode: p.platform_code,
              children: (p.contents || []).map(ct => ({
                value: 'ct_' + ct, label: ct, isLeaf: true,
                customerId: c.id, platformCode: p.platform_code, promoContent: ct
              }))
            }))
          })).filter(c => c.children && c.children.length)
        }
      } catch (e) {
        this.$message.error('加载打款对象/客户数据失败，请检查后端服务')
      }
    },
    onTypeChange() {
      this.form.cascade = []
      this.form.generated_count = 0
      this.form.heat_value = 0
      this.form.payable_amount = ''
      this.form.customer_id = null
      this.form.platform_code = ''
      this.form.promo_content = ''
    },
    findLeaf(cascade, options) {
      let nodes = options
      let node = null
      for (const v of cascade) {
        node = (nodes || []).find(x => x.value === v)
        if (!node) return null
        nodes = node.children
      }
      return node
    },
    async onCascadeChange(val) {
      this.form.generated_count = 0
      this.form.heat_value = 0
      this.form.payable_amount = ''
      this.form.customer_id = null
      this.form.platform_code = ''
      this.form.promo_content = ''
      if (!val || val.length < 3) return
      if (this.form.launch_type === 'NOVEL_PROMO') {
        const node = this.findLeaf(val, this.novelOptions)
        if (!node || !node.customerId) return
        this.form.customer_id = node.customerId
        this.form.platform_code = node.platformCode
        this.form.promo_content = node.promoContent
        const { data } = await previewNovelWithdraw(node.customerId,
          { platform_code: node.platformCode, promo_content: node.promoContent })
        if (data.code === 0) {
          this.form.generated_count = data.data.generated_count || 0
          if (!this.form.generated_count) this.$message.warning('该客户网文推广剩余可出款条数为0，不允许提交')
        } else { this.$message.warning(data.msg || '无网文推广投放数据') }
        return
      }
      const node = this.findLeaf(val, this.customerOptions)
      if (!node || !node.accountId) return
      const { data } = await previewWithdraw(node.accountId, this.form.launch_type)
      if (data.code === 0) {
        const d = data.data
        this.form.generated_count = d.generated_count || 0
        this.form.heat_value = d.heat_value || 0
        if (this.form.launch_type === 'FIRST_CHARGE' && !this.form.generated_count) {
          this.$message.warning('该ID剩余可出款条数为0，不允许提交')
        }
        if (this.form.launch_type === 'EXPOSURE' && !this.form.heat_value) {
          this.$message.warning('该ID曝光度剩余可出款热度为0，不允许提交')
        }
      }
    },
    async onSubmit() {
      if (!this.form.payee_id) { this.$message.warning('请选择打款对象'); return }
      if (!this.form.launch_type) { this.$message.warning('请先选择类型'); return }
      if (!this.form.cascade || this.form.cascade.length < 3) {
        this.$message.warning(this.form.launch_type === 'NOVEL_PROMO' ? '请选择客户 → 平台 → 内容' : '请选择客户 → 平台 → ID'); return
      }
      if ((this.form.launch_type === 'FIRST_CHARGE' || this.form.launch_type === 'NOVEL_PROMO')
          && !(Number(this.form.generated_count) > 0)) {
        this.$message.warning('剩余生成条数为0，不允许提交'); return
      }
      if (this.form.launch_type === 'EXPOSURE' && !(Number(this.form.heat_value) > 0)) {
        this.$message.warning('剩余热度为0，不允许提交'); return
      }
      const amt = Number(this.form.payable_amount)
      if (!amt || isNaN(amt) || amt <= 0) { this.$message.warning('请填写正确的结算金额'); return }
      if (!this.form.settle_date) { this.$message.warning('请选择结算日期'); return }
      const payload = {
        payee_id: this.form.payee_id,
        launch_type: this.form.launch_type,
        generated_count: Number(this.form.generated_count || 0),
        heat_value: Number(this.form.heat_value || 0),
        payable_amount: amt,
        settle_date: this.form.settle_date,
        remark: this.form.remark
      }
      if (this.form.launch_type === 'NOVEL_PROMO') {
        if (!this.form.customer_id) { this.$message.warning('网文推广出款数据无效'); return }
        payload.customer_id = this.form.customer_id
        payload.platform_code = this.form.platform_code
        payload.promo_content = this.form.promo_content
      } else {
        const node = this.findLeaf(this.form.cascade, this.customerOptions)
        if (!node || !node.accountId) { this.$message.warning('投放ID无效'); return }
        payload.douyin_account_id = node.accountId
      }
      this.submitting = true
      try {
        const { data } = await createWithdraw(payload)
        if (data.code === 0) {
          this.$alert('出款成功，结算金额：￥' + Number(data.data.payable_amount || 0).toFixed(2), '提示',
            { confirmButtonText: '确定', type: 'success' }).then(() => {
              this.dialogVisible = false; this.load(1)
            })
        } else { this.$message.error(data.msg || '提交失败') }
      } finally { this.submitting = false }
    },
    onDelete(row) {
      this.$confirm('确认删除该出款记录？', '提示', { type: 'warning' })
        .then(async () => {
          const { data } = await deleteWithdraw(row.id)
          if (data.code === 0) { this.$message.success('删除成功'); this.load(1) }
          else this.$message.error(data.msg || '删除失败')
        }).catch(() => {})
    },
    onExport() {
      if (!this.query.launch_type) { this.$message.warning('导出前必须先选择类型（首充/曝光度/网文推广）'); return }
      const q = new URLSearchParams()
      q.append('launch_type', this.query.launch_type)
      if (this.query.keyword) q.append('keyword', this.query.keyword)
      if (this.dateRange && this.dateRange.length === 2) {
        q.append('date_from', this.dateRange[0])
        q.append('date_to', this.dateRange[1])
      }
      fetch(withdrawExportUrl + '?' + q.toString(),
            { headers: { Authorization: 'Bearer ' + getAdminToken() } })
        .then(async r => {
          const ct = r.headers.get('content-type') || ''
          if (ct.indexOf('json') !== -1) { const j = await r.json(); this.$message.error(j.msg || '导出失败'); return null }
          return r.blob()
        })
        .then(b => {
          if (!b) return
          const a = document.createElement('a')
          a.href = URL.createObjectURL(b)
          const typeLabel = this.query.launch_type === 'EXPOSURE' ? '直播曝光度'
            : (this.query.launch_type === 'NOVEL_PROMO' ? '网文推广' : '首充')
          a.download = `出款_${typeLabel}_${new Date().toISOString().slice(0,10)}.xlsx`
          a.click()
          URL.revokeObjectURL(a.href)
          this.$message.success('导出成功')
        }).catch(() => this.$message.error('导出失败'))
    }
  }
}
</script>