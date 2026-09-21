<template>
  <div class="client-sub">
    <div class="topbar flex-between">
      <div class="logo">恒耀互娱 - 财务</div>
      <div><el-button type="text" @click="$router.push('/client/home')">返回首页</el-button></div>
    </div>
    <div class="page-container">
      <div class="card">
        <div class="card-title">我的资金</div>
        <el-table :data="rows" border stripe>
          <el-table-column prop="douyin_name" label="抖音号" />
          <el-table-column prop="douyin_id" label="抖音ID" />
          <el-table-column prop="recharge_amount" label="充值金额(元)" width="130" />
          <el-table-column prop="balance" label="剩余流水(元)" width="130" />
          <el-table-column prop="tier" label="档位" width="80" />
          <el-table-column prop="tier_daily_budget" label="日预算" width="100" />
        </el-table>
        <div class="text-muted mt-16">交易均为线下处理，此处仅作登记展示，如需充值请联系客服。</div>
      </div>

      <div class="card mt-16">
        <div class="flex-between">
          <div class="card-title" style="margin-bottom:0">我的开票申请</div>
          <el-button type="primary" size="small" class="hy-cta" icon="el-icon-tickets" @click="openApply">申请开票</el-button>
        </div>
        <el-table :data="invoices" border stripe v-loading="invLoading" class="mt-16">
          <el-table-column prop="id" label="申请ID" width="90" />
          <el-table-column label="抖音ID" width="140">
            <template slot-scope="{ row }">{{ row.douyin_id || '-' }}</template>
          </el-table-column>
          <el-table-column prop="amount" label="开票金额(元)" width="140" />
          <el-table-column label="状态" width="110">
            <template slot-scope="{ row }">
              <el-tag :type="row.status==='PENDING'?'warning':'success'" size="mini">
                {{ row.status === 'PENDING' ? '待处理' : '已完成' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="申请时间" width="180">
            <template slot-scope="{ row }">{{ fmt(row.invoice_at) }}</template>
          </el-table-column>
          <el-table-column label="完成时间" width="180">
            <template slot-scope="{ row }">{{ row.processed_at ? fmt(row.processed_at) : '-' }}</template>
          </el-table-column>
          <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        </el-table>
        <el-pagination class="mt-16" background layout="total, prev, pager, next"
                       :total="invTotal" :current-page="invQuery.page" :page-size="invQuery.page_size"
                       @current-change="p => loadInvoices(p)" />
      </div>
    </div>

    <el-dialog title="申请开票" :visible.sync="applyVisible" width="440px" :close-on-click-modal="false">
      <el-form ref="aform" :model="aform" :rules="arules" label-width="90px" size="small">
        <el-form-item label="抖音ID" prop="douyin_id">
          <el-select v-model="aform.douyin_id" filterable placeholder="请选择要开票的抖音ID" style="width:100%">
            <el-option v-for="a in accounts" :key="a.douyin_id"
                       :label="a.douyin_id + (a.douyin_name ? '（' + a.douyin_name + '）' : '')"
                       :value="a.douyin_id" />
          </el-select>
        </el-form-item>
        <el-form-item label="开票金额" prop="amount">
          <el-input v-model="aform.amount" placeholder="正数,单位元" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="aform.remark" type="textarea" :rows="3" maxlength="255" placeholder="选填,如发票抬头等" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button size="small" @click="applyVisible=false">取消</el-button>
        <el-button size="small" type="primary" :loading="saving" @click="submitApply">提交申请</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { applyInvoice, listMyInvoices } from '@/api/clientInvoice'
import { isPositiveNumber } from '@/utils/validate'
export default {
  name: 'ClientFinance',
  data() {
    return {
      invLoading: false, saving: false, applyVisible: false,
      invoices: [], invTotal: 0, invQuery: { page: 1, page_size: 10 },
      aform: { douyin_id: '', amount: '', remark: '' },
      arules: {
        douyin_id: [{ required: true, message: '请选择抖音ID', trigger: 'change' }],
        amount: [
          { required: true, message: '请输入开票金额', trigger: 'blur' },
          { validator: (r, v, cb) => isPositiveNumber(v) ? cb() : cb(new Error('请输入大于0的金额')), trigger: 'blur' }
        ]
      }
    }
  },
  computed: { ...mapState('clientUser', ['accounts']), rows() { return this.accounts || [] } },
  async created() {
    if (!this.accounts.length) await this.$store.dispatch('clientUser/loadAccounts')
    this.loadInvoices(1)
  },
  methods: {
    fmt(t) { return t ? String(t).replace('T', ' ').slice(0, 19) : '-' },
    async loadInvoices(page) {
      this.invQuery.page = page || this.invQuery.page
      this.invLoading = true
      try {
        const { data } = await listMyInvoices(this.invQuery)
        if (data.code === 0) { this.invoices = data.data.items; this.invTotal = data.data.total }
      } finally { this.invLoading = false }
    },
    openApply() {
      this.aform = { douyin_id: '', amount: '', remark: '' }
      this.applyVisible = true
      this.$nextTick(() => this.$refs.aform && this.$refs.aform.clearValidate())
    },
    submitApply() {
      this.$refs.aform.validate(async ok => {
        if (!ok) return
        this.saving = true
        try {
          const { data } = await applyInvoice({ ...this.aform, amount: Number(this.aform.amount) })
          if (data.code === 0) {
            this.$message.success('申请已提交,请等待客服处理')
            this.applyVisible = false
            this.loadInvoices(1)
          }
        } finally { this.saving = false }
      })
    }
  }
}
</script>

<style scoped lang="scss">
.client-sub { min-height: 100vh; background: linear-gradient(160deg, #fff0f5 0%, #ffe8ef 45%, #ffeef4 100%); }
.topbar {
  height: 56px; padding: 0 24px;
  background: linear-gradient(135deg, #ff5f8f 0%, #ff2e63 100%);
  box-shadow: 0 2px 12px rgba(255, 46, 99, .25);
  .logo { font-weight: bold; font-size: 18px; color: #fff; }
  ::v-deep .el-button--text { color: #fff; }
}
.card {
  background: #fff; padding: 18px; border-radius: 12px;
  box-shadow: 0 4px 16px rgba(255, 46, 99, .08);
  .card-title { font-size: 15px; font-weight: bold; margin-bottom: 12px;
    border-left: 3px solid #ff2e63; padding-left: 8px; }
}
</style>
