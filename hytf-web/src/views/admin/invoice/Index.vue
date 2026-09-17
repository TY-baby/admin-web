<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form :inline="true" size="small">
        <el-form-item label="鐘舵€?>
          <el-select v-model="query.status" placeholder="鍏ㄩ儴" clearable style="width:140px">
            <el-option label="寰呭鐞? value="PENDING" />
            <el-option label="宸插紑绁? value="PROCESSED" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">鏌ヨ</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">閲嶇疆</el-button>
          <el-button type="success" icon="el-icon-plus" @click="openCreate">鏂板寮€绁ㄨ褰?/el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="customer_name" label="瀹㈡埛鍚嶇О" />
        <el-table-column prop="amount" label="寮€绁ㄩ噾棰?鍏?" width="140" />
        <el-table-column label="寮€绁ㄦ椂闂? width="180">
          <template slot-scope="{ row }">{{ String(row.invoice_at).replace('T',' ').slice(0,19) }}</template>
        </el-table-column>
        <el-table-column label="鐘舵€? width="100">
          <template slot-scope="{ row }">
            <el-tag :type="row.status==='PENDING'?'warning':'success'" size="mini">
              {{ row.status === 'PENDING' ? '寰呭鐞? : '宸插紑绁? }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="澶囨敞" show-overflow-tooltip />
        <el-table-column label="鎿嶄綔" width="140" fixed="right">
          <template slot-scope="{ row }">
            <el-button v-if="row.status === 'PENDING'" size="mini" type="primary" @click="onProcess(row)">宸插鐞?/el-button>
            <span v-else class="text-muted">宸插畬鎴?/span>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="mt-16" background layout="total, sizes, prev, pager, next, jumper"
                     :total="total" :current-page="query.page" :page-size="query.page_size"
                     :page-sizes="[10,20,50,100]"
                     @current-change="p => load(p)"
                     @size-change="s => { query.page_size = s; load(1) }" />
    </el-card>

    <el-dialog title="鏂板寮€绁ㄨ褰? :visible.sync="createVisible" width="480px" :close-on-click-modal="false">
      <el-form ref="cform" :model="cform" :rules="crules" label-width="100px" size="small">
        <el-form-item label="瀹㈡埛鍚嶇О" prop="customer_name">
          <el-input v-model="cform.customer_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="寮€绁ㄩ噾棰? prop="amount">
          <el-input v-model="cform.amount" placeholder="姝ｆ暟,鍗曚綅鍏? />
        </el-form-item>
        <el-form-item label="澶囨敞">
          <el-input v-model="cform.remark" type="textarea" :rows="3" maxlength="255" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button size="small" @click="createVisible=false">鍙栨秷</el-button>
        <el-button size="small" type="primary" :loading="saving" @click="submitCreate">淇濆瓨</el-button>
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
        customer_name: [{ required: true, message: '璇疯緭鍏ュ鎴峰悕绉?, trigger: 'blur' }],
        amount: [
          { required: true, message: '璇疯緭鍏ュ紑绁ㄩ噾棰?, trigger: 'blur' },
          { validator: (r, v, cb) => isPositiveNumber(v) ? cb() : cb(new Error('璇疯緭鍏ュぇ浜?鐨勯噾棰?)), trigger: 'blur' }
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
            this.$message.success('宸插垱寤?)
            this.createVisible = false
            this.load(1)
          }
        } finally { this.saving = false }
      })
    },
    onProcess(row) {
      this.$confirm('纭灏嗗紑绁ㄨ褰曘€怚D:' + row.id + ', 閲戦:' + row.amount + '銆戞爣璁颁负宸插紑绁紵',
        '浜屾纭', { type: 'warning', confirmButtonText: '鎻愪氦', cancelButtonText: '鍙栨秷' })
        .then(async () => {
          const { data } = await processInvoice(row.id)
          if (data.code === 0) { this.$message.success('宸叉爣璁颁负宸插紑绁?); this.load() }
        }).catch(() => {})
    }
  }
}
</script>