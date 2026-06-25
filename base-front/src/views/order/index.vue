<template>
  <div>
    <el-form :inline='true' size='small'>
      <el-form-item label='关键字'><el-input v-model='query.keyword' clearable /></el-form-item>
      <el-form-item label='状态'>
        <el-select v-model='query.status' clearable>
          <el-option v-for='item in dicts.order_status' :key='item.id' :label='item.dict_label' :value='item.dict_value' />
        </el-select>
      </el-form-item>
      <el-form-item><el-button type='primary' @click='load'>查询</el-button></el-form-item>
      <el-form-item><el-button type='success' @click='openDialog()'>新增订单</el-button></el-form-item>
    </el-form>
    <el-table :data='list' v-loading='loading' border>
      <el-table-column prop='order_no' label='订单编号' />
      <el-table-column prop='customer_name' label='客户' />
      <el-table-column prop='amount' label='金额' />
      <el-table-column prop='actual_amount' label='实付金额' />
      <el-table-column prop='status' label='状态' />
      <el-table-column prop='pay_status' label='付款状态' />
      <el-table-column prop='order_date' label='下单日期' />
      <el-table-column label='操作' width='150'>
        <template slot-scope='scope'>
          <el-button type='text' @click='openDialog(scope.row)'>编辑</el-button>
          <el-button type='text' style='color:#f56c6c' @click='remove(scope.row.id)'>删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination :current-page.sync='query.page' :page-size='query.size' :total='total' layout='total, prev, pager, next' @current-change='load' style='margin-top: 15px;' />
    <el-dialog :title='form.id ? "编辑订单" : "新增订单"' :visible.sync='visible' width='700px'>
      <el-form :model='form' label-width='100px'>
        <el-form-item label='客户ID'><el-input v-model='form.customer_id' /></el-form-item>
        <el-form-item label='关联商机'><el-input v-model='form.opportunity_id' /></el-form-item>
        <el-form-item label='金额'><el-input v-model='form.amount' /></el-form-item>
        <el-form-item label='折扣'><el-input v-model='form.discount' /></el-form-item>
        <el-form-item label='实付金额'><el-input v-model='form.actual_amount' /></el-form-item>
        <el-form-item label='状态'>
          <el-select v-model='form.status'>
            <el-option v-for='item in dicts.order_status' :key='item.id' :label='item.dict_label' :value='item.dict_value' />
          </el-select>
        </el-form-item>
        <el-form-item label='付款状态'><el-select v-model='form.pay_status'><el-option label='未付款' value='未付款' /><el-option label='已付款' value='已付款' /><el-option label='部分付款' value='部分付款' /></el-select></el-form-item>
        <el-form-item label='下单日期'><el-date-picker v-model='form.order_date' value-format='yyyy-MM-dd' /></el-form-item>
        <el-form-item label='交付日期'><el-date-picker v-model='form.delivery_date' value-format='yyyy-MM-dd' /></el-form-item>
        <el-form-item label='备注'><el-input v-model='form.remark' type='textarea' /></el-form-item>
      </el-form>
      <div slot='footer'><el-button @click='visible=false'>取消</el-button><el-button type='primary' @click='submit'>确定</el-button></div>
    </el-dialog>
  </div>
</template>

<script>
import { getOrderList, createOrder, updateOrder, deleteOrder } from '@/api/order'
import { getAllDicts } from '@/api/dashboard'
export default {
  data() { return { loading: false, list: [], total: 0, visible: false, query: { keyword: '', status: '', page: 1, size: 10 }, form: {}, dicts: { order_status: [] } } },
  created() { this.loadDicts(); this.load() },
  methods: {
    async loadDicts() { this.dicts = await getAllDicts() },
    async load() { this.loading = true; const res = await getOrderList(this.query); this.list = res.list; this.total = res.total; this.loading = false },
    openDialog(row = {}) { this.form = { ...row }; this.visible = true },
    async submit() { if (this.form.id) await updateOrder(this.form.id, this.form); else await createOrder(this.form); this.$message.success('操作成功'); this.visible = false; this.load() },
    async remove(id) { await this.$confirm('确认删除?', '提示', { type: 'warning' }); await deleteOrder(id); this.$message.success('删除成功'); this.load() }
  }
}
</script>
