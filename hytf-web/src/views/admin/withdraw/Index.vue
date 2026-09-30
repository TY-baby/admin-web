<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form :inline="true" :model="query" size="small">
        <el-form-item label="名称">
          <el-input v-model="query.keyword_name" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="打款日期">
          <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd"
                          start-placeholder="开始" end-placeholder="结束" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">查询</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">重置</el-button>
          <el-button type="success" icon="el-icon-plus" @click="openAdd">新增出款</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="pay_date" label="打款日期" width="130" />
        <el-table-column prop="id_count" label="产出ID数量" width="120" />
        <el-table-column label="应付金额(元)" width="130">
          <template slot-scope="{ row }">{{ Number(row.payable_amount || 0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
        <el-table-column label="登记时间" width="160">
          <template slot-scope="{ row }">{{ row.created_at ? String(row.created_at).replace('T',' ').slice(0,19) : '-' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="90" fixed="right">
          <template slot-scope="{ row }">
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

    <el-dialog title="新增出款登记" :visible.sync="addVisible" width="500px" :close-on-click-modal="false">
      <el-form ref="aform" :model="aform" :rules="arules" label-width="110px" size="small">
        <el-form-item label="名称" prop="name">
          <el-input v-model="aform.name" maxlength="50" placeholder="出款对象名称" />
        </el-form-item>
        <el-form-item label="打款日期" prop="pay_date">
          <el-date-picker v-model="aform.pay_date" type="date" value-format="yyyy-MM-dd"
                          placeholder="选择日期" style="width:100%" />
        </el-form-item>
        <el-form-item label="产出ID数量" prop="id_count">
          <el-input-number v-model="aform.id_count" :min="0" :max="999999" />
        </el-form-item>
        <el-form-item label="应付金额(元)" prop="payable_amount">
          <el-input v-model="aform.payable_amount" placeholder="正数,单位元" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="aform.remark" type="textarea" :rows="2" maxlength="255" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button size="small" @click="addVisible=false">取消</el-button>
        <el-button size="small" type="primary" :loading="saving" @click="submitAdd">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listWithdraws, createWithdraw, deleteWithdraw } from '@/api/adminWithdraw'
import { isPositiveNumber } from '@/utils/validate'

export default {
  name: 'AdminWithdraw',
  data() {
    return {
      loading: false, saving: false, addVisible: false,
      rows: [], total: 0, dateRange: [],
      query: { keyword_name: '', page: 1, page_size: 20 },
      aform: { name: '', pay_date: '', id_count: 0, payable_amount: '', remark: '' },
      arules: {
        name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        pay_date: [{ required: true, message: '请选择打款日期', trigger: 'change' }],
        payable_amount: [
          { required: true, message: '请输入应付金额', trigger: 'blur' },
          { validator: (r, v, cb) => isPositiveNumber(v) ? cb() : cb(new Error('请输入大于0的金额')), trigger: 'blur' }
        ]
      }
    }
  },
  created() { this.load(1) },
  methods: {
    async load(page) {
      this.query.page = page || this.query.page
      const params = { ...this.query }
      if (this.dateRange && this.dateRange.length === 2) {
        params.date_from = this.dateRange[0]
        params.date_to = this.dateRange[1]
      }
      this.loading = true
      try {
        const { data } = await listWithdraws(params)
        if (data.code === 0) { this.rows = data.data.items; this.total = data.data.total }
      } finally { this.loading = false }
    },
    reset() {
      this.query = { keyword_name: '', page: 1, page_size: 20 }
      this.dateRange = []
      this.load(1)
    },
    openAdd() {
      this.aform = { name: '', pay_date: '', id_count: 0, payable_amount: '', remark: '' }
      this.addVisible = true
      this.$nextTick(() => this.$refs.aform && this.$refs.aform.clearValidate())
    },
    submitAdd() {
      this.$refs.aform.validate(async ok => {
        if (!ok) return
        this.saving = true
        try {
          const { data } = await createWithdraw({
            name: this.aform.name,
            pay_date: this.aform.pay_date,
            id_count: this.aform.id_count,
            payable_amount: Number(this.aform.payable_amount),
            remark: this.aform.remark
          })
          if (data.code === 0) { this.$message.success('已保存'); this.addVisible = false; this.load(1) }
          else { this.$message.error(data.msg || '保存失败') }
        } finally { this.saving = false }
      })
    },
    onDelete(row) {
      this.$confirm('确定删除出款记录【' + row.name + '】吗?', '警告', { type: 'warning' })
          .then(async () => {
            const { data } = await deleteWithdraw(row.id)
            if (data.code === 0) { this.$message.success('已删除'); this.load(this.query.page) }
          }).catch(() => {})
    }
  }
}
</script>