<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form :inline="true" size="small">
        <el-form-item label="状态">
          <el-select v-model="query.status" placeholder="全部" clearable style="width:140px">
            <el-option label="待处理" value="PENDING" />
            <el-option label="已开票" value="PROCESSED" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">查询</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">重置</el-button>
          <el-button type="success" icon="el-icon-plus" @click="openCreate">新增开票记录</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="customer_name" label="客户名称" />
        <el-table-column prop="amount" label="开票金额(元)" width="140" />
        <el-table-column label="开票时间" width="180">
          <template slot-scope="{ row }">{{ String(row.invoice_at).replace('T',' ').slice(0,19) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="{ row }">
            <el-tag :type="row.status==='PENDING'?'warning':'success'" size="mini">
              {{ row.status === 'PENDING' ? '待处理' : '已开票' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        <el-table-column label="操作" width="140" fixed="right">
          <template slot-scope="{ row }">
            <el-button v-if="row.status === 'PENDING'" size="mini" type="primary" @click="onProcess(row)">已处理</el-button>
            <span v-else class="text-muted">已完成</span>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="mt-16" background layout="total, sizes, prev, pager, next, jumper"
                     :total="total" :current-page="query.page" :page-size="query.page_size"
                     :page-sizes="[10,20,50,100]"
                     @current-change="p => load(p)"
                     @size-change="s => { query.page_size = s; load(1) }" />
    </el-card>

    <el-dialog title="新增开票记录" :visible.sync="createVisible" width="480px" :close-on-click-modal="false">
      <el-form ref="cform" :model="cform" :rules="crules" label-width="100px" size="small">
        <el-form-item label="客户名称" prop="customer_name">
          <el-input v-model="cform.customer_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="开票金额" prop="amount">
          <el-input v-model="cform.amount" placeholder="正数,单位元" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="cform.remark" type="textarea" :rows="3" maxlength="255" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button size="small" @click="createVisible=false">取消</el-button>
        <el-button size="small" type="primary" :loading="saving" @click="submitCreate">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listInvoices, createInvoice, processInvoice } from '@/api/adminInvoice'
import { isPositiveNumber } from '@/utils/validate'

export default {
  name: 'AdminInvoice',
  data() {
    return {
      loading: false, saving: false, rows: [], total: 0,
      query: { status: '', page: 1, page_size: 20 },
      createVisible: false,
      cform: { customer_name: '', amount: '', remark: '' },
      crules: {
        customer_name: [{ required: true, message: '请输入客户名称', trigger: 'blur' }],
        amount: [
          { required: true, message: '请输入开票金额', trigger: 'blur' },
          { validator: (r, v, cb) => isPositiveNumber(v) ? cb() : cb(new Error('请输入大于0的金额')), trigger: 'blur' }
        ]
      }
    }
  },
  created() { this.load(1) },
  methods: {
    async load(page) {
      this.query.page = page || this.query.page
      this.loading = true
      try {
        const { data } = await listInvoices(this.query)
        if (data.code === 0) { this.rows = data.data.items; this.total = data.data.total }
      } finally { this.loading = false }
    },
    reset() { this.query = { status: '', page: 1, page_size: 20 }; this.load(1) },
    openCreate() {
      this.cform = { customer_name: '', amount: '', remark: '' }
      this.createVisible = true
      this.$nextTick(() => this.$refs.cform && this.$refs.cform.clearValidate())
    },
    submitCreate() {
      this.$refs.cform.validate(async ok => {
        if (!ok) return
        this.saving = true
        try {
          const { data } = await createInvoice({ ...this.cform, amount: Number(this.cform.amount) })
          if (data.code === 0) {
            this.$message.success('已创建')
            this.createVisible = false
            this.load(1)
          }
        } finally { this.saving = false }
      })
    },
    onProcess(row) {
      this.$confirm('确认将开票记录【ID:' + row.id + ', 金额:' + row.amount + '】标记为已开票？',
        '二次确认', { type: 'warning', confirmButtonText: '提交', cancelButtonText: '取消' })
        .then(async () => {
          const { data } = await processInvoice(row.id)
          if (data.code === 0) { this.$message.success('已标记为已开票'); this.load() }
        }).catch(() => {})
    }
  }
}
</script>