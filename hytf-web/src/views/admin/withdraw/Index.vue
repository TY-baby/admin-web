<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form :inline="true" :model="query" size="small">
        <el-form-item label="关键词">
          <el-input v-model="query.keyword" placeholder="打款对象/客户/投放ID" clearable />
        </el-form-item>
        <el-form-item label="创建时间">
          <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd"
                          start-placeholder="开始" end-placeholder="结束" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">查询</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">重置</el-button>
          <el-button type="success" icon="el-icon-plus" @click="openDialog">新增出款</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column prop="payee_holder_name" label="打款对象" width="110" />
        <el-table-column prop="payee_bank_name" label="开户行" min-width="180" show-overflow-tooltip />
        <el-table-column prop="payee_card_no" label="卡号" width="200" />
        <el-table-column prop="customer_name" label="客户名称" width="120" />
        <el-table-column prop="douyin_id" label="投放ID" width="130" />
        <el-table-column prop="douyin_name" label="ID昵称" width="120" />
        <el-table-column prop="generated_count" label="生成条数" width="90" align="center" />
        <el-table-column label="打款金额(元)" width="120" align="right">
          <template slot-scope="{ row }">{{ Number(row.payable_amount || 0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column prop="operator" label="操作人" width="90" />
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="80" fixed="right">
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

    <el-dialog title="新增出款" :visible.sync="dialogVisible" width="560px"
               :close-on-click-modal="false" @open="onDialogOpen">
      <el-form :model="form" label-width="100px" size="small">
        <el-form-item label="打款对象" required>
          <el-select v-model="form.payee_id" placeholder="请选择打款对象" style="width:100%"
                     @change="onPayeeChange">
            <el-option v-for="p in payees" :key="p.id" :label="p.display_name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="selectedPayee" label="开户行">
          <span>{{ selectedPayee.bank_name }}</span>
        </el-form-item>
        <el-form-item v-if="selectedPayee" label="卡号">
          <span>{{ selectedPayee.card_no }}</span>
        </el-form-item>
        <el-form-item label="客户/ID" required>
          <el-cascader v-model="form.cascade" :options="customerOptions"
                       :props="cascaderProps" placeholder="请选择客户及投放ID"
                       style="width:100%" filterable clearable
                       @change="onCascadeChange" />
        </el-form-item>
        <el-form-item v-if="preview" label="生成条数">
          <span>{{ preview.generated_count }} 条</span>
        </el-form-item>
        <el-form-item v-if="preview" label="打款金额">
          <span style="color:#F56C6C;font-weight:bold;font-size:16px">
            ￥{{ Number(preview.payable_amount || 0).toFixed(2) }}
          </span>
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
import { listWithdraws, listPayees, listWithdrawCustomers, previewWithdraw, createWithdraw, deleteWithdraw } from '@/api/adminWithdraw'

export default {
  name: 'AdminWithdraw',
  data() {
    return {
      loading: false, rows: [], total: 0, dateRange: [],
      query: { keyword: '', page: 1, page_size: 20 },
      dialogVisible: false, submitting: false,
      payees: [], customerOptions: [],
      form: { payee_id: null, cascade: [], remark: '' },
      preview: null,
      cascaderProps: { value: 'id', label: 'label', children: 'children' }
    }
  },
  computed: {
    selectedPayee() {
      return this.payees.find(p => p.id === this.form.payee_id) || null
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
      this.query = { keyword: '', page: 1, page_size: 20 }
      this.dateRange = []
      this.load(1)
    },
    openDialog() {
      this.dialogVisible = true
    },
    async onDialogOpen() {
      this.form = { payee_id: null, cascade: [], remark: '' }
      this.preview = null
      try {
        const [pRes, cRes] = await Promise.all([listPayees(), listWithdrawCustomers()])
        if (pRes.data.code === 0) this.payees = pRes.data.data || []
        if (cRes.data.code === 0) {
          this.customerOptions = (cRes.data.data || []).map(c => ({
            id: 'c_' + c.id, label: c.customer_name,
            children: (c.accounts || []).map(a => ({
              id: a.id, label: a.douyin_id + (a.douyin_name ? '（' + a.douyin_name + '）' : '')
            }))
          }))
        }
      } catch (e) {
        this.$message.error('加载打款对象/客户数据失败，请检查后端服务')
      }
    },
    onPayeeChange() {},
    async onCascadeChange(val) {
      this.preview = null
      if (!val || val.length < 2) return
      const accountId = val[1]
      const { data } = await previewWithdraw(accountId)
      if (data.code === 0) this.preview = data.data
    },
    async onSubmit() {
      if (!this.form.payee_id) { this.$message.warning('请选择打款对象'); return }
      if (!this.form.cascade || this.form.cascade.length < 2) { this.$message.warning('请选择客户及投放ID'); return }
      this.submitting = true
      try {
        const { data } = await createWithdraw({
          payee_id: this.form.payee_id,
          douyin_account_id: this.form.cascade[1],
          remark: this.form.remark
        })
        if (data.code === 0) {
          this.$alert('出款成功，打款金额：￥' + Number(data.data.payable_amount || 0).toFixed(2), '提示', {
            confirmButtonText: '确定', type: 'success'
          }).then(() => {
            this.dialogVisible = false
            this.load(1)
          })
        } else {
          this.$message.error(data.msg || '提交失败')
        }
      } finally { this.submitting = false }
    },
    onDelete(row) {
      this.$confirm('确认删除该出款记录？', '提示', { type: 'warning' })
        .then(async () => {
          const { data } = await deleteWithdraw(row.id)
          if (data.code === 0) { this.$message.success('删除成功'); this.load(1) }
          else this.$message.error(data.msg || '删除失败')
        }).catch(() => {})
    }
  }
}
</script>