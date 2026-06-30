<template>
  <div>
    <el-form :inline='true' size='small'>
      <el-form-item label='关键字'><el-input v-model='query.keyword' placeholder='客户名称/电话/公司' clearable /></el-form-item>
      <el-form-item label='状态'>
        <el-select v-model='query.status' placeholder='全部' clearable>
          <el-option v-for='item in dicts.customer_status' :key='item.id' :label='item.dict_label' :value='item.dict_value' />
        </el-select>
      </el-form-item>
      <el-form-item><el-button type='primary' icon='el-icon-search' @click='load'>查询</el-button></el-form-item>
      <el-form-item><el-button type='success' icon='el-icon-plus' @click='openDialog()'>新增客户</el-button></el-form-item>
    </el-form>
    <el-table :data='list' v-loading='loading' border>
      <el-table-column type='index' width='50' />
      <el-table-column prop='name' label='客户名称' />
      <el-table-column prop='phone' label='电话' />
      <el-table-column prop='company' label='公司' />
      <el-table-column prop='industry' label='行业' />
      <el-table-column prop='source' label='来源' />
      <el-table-column prop='status' label='状态' />
      <el-table-column prop='level' label='等级' />
      <el-table-column label='操作' width='180'>
        <template slot-scope='scope'>
          <el-button type='text' @click='$router.push("/crm/customer/detail/" + scope.row.id)'>详情</el-button>
          <el-button type='text' @click='openDialog(scope.row)'>编辑</el-button>
          <el-button type='text' style='color:#f56c6c' @click='remove(scope.row.id)'>删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination :current-page.sync='query.page' :page-size='query.size' :total='total' layout='total, prev, pager, next' @current-change='load' style='margin-top: 15px;' />
    <el-dialog :title='form.id ? "编辑客户" : "新增客户"' :visible.sync='visible' width='600px'>
      <el-form :model='form' label-width='80px'>
        <el-form-item label='客户名称'><el-input v-model='form.name' /></el-form-item>
        <el-form-item label='电话'><el-input v-model='form.phone' /></el-form-item>
        <el-form-item label='邮箱'><el-input v-model='form.email' /></el-form-item>
        <el-form-item label='公司'><el-input v-model='form.company' /></el-form-item>
        <el-form-item label='行业'><el-input v-model='form.industry' /></el-form-item>
        <el-form-item label='来源'>
          <el-select v-model='form.source' placeholder='请选择'>
            <el-option v-for='item in sources' :key='item' :label='item' :value='item' />
          </el-select>
        </el-form-item>
        <el-form-item label='状态'>
          <el-select v-model='form.status' placeholder='请选择'>
            <el-option v-for='item in dicts.customer_status' :key='item.id' :label='item.dict_label' :value='item.dict_value' />
          </el-select>
        </el-form-item>
        <el-form-item label='等级'>
          <el-select v-model='form.level' placeholder='请选择'>
            <el-option label='A级' value='A级' /><el-option label='B级' value='B级' /><el-option label='C级' value='C级' />
          </el-select>
        </el-form-item>
        <el-form-item label='备注'><el-input v-model='form.remark' type='textarea' /></el-form-item>
      </el-form>
      <div slot='footer'><el-button @click='visible=false'>取消</el-button><el-button type='primary' @click='submit'>确定</el-button></div>
    </el-dialog>
  </div>
</template>

<script>
import { getCustomerList, createCustomer, updateCustomer, deleteCustomer } from '@/api/customer'
import { getAllDicts } from '@/api/dashboard'
export default {
  data() {
    return {
      loading: false, list: [], total: 0, visible: false,
      query: { keyword: '', status: '', page: 1, size: 10 },
      form: {}, dicts: { customer_status: [] }, sources: ['官网','推广','转介绍','展会','电话','其他']
    }
  },
  created() { this.loadDicts(); this.load() },
  methods: {
    async loadDicts() { this.dicts = await getAllDicts() },
    async load() {
      this.loading = true
      const res = await getCustomerList(this.query)
      this.list = res.list; this.total = res.total; this.loading = false
    },
    openDialog(row = {}) { this.form = { ...row }; this.visible = true },
    async submit() {
      if (this.form.id) await updateCustomer(this.form.id, this.form)
      else await createCustomer(this.form)
      this.$message.success('操作成功'); this.visible = false; this.load()
    },
    async remove(id) {
      await this.$confirm('确认删除?', '提示', { type: 'warning' })
      await deleteCustomer(id); this.$message.success('删除成功'); this.load()
    }
  }
}
</script>
