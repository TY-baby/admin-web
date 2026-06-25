<template>
  <div>
    <el-form :inline='true' size='small'>
      <el-form-item label='关键字'><el-input v-model='query.keyword' clearable /></el-form-item>
      <el-form-item><el-button type='primary' @click='load'>查询</el-button></el-form-item>
      <el-form-item><el-button type='success' @click='openDialog()'>新增产品</el-button></el-form-item>
    </el-form>
    <el-table :data='list' v-loading='loading' border>
      <el-table-column prop='code' label='编码' />
      <el-table-column prop='name' label='名称' />
      <el-table-column prop='category' label='分类' />
      <el-table-column prop='price' label='价格' />
      <el-table-column prop='stock' label='库存' />
      <el-table-column prop='unit' label='单位' />
      <el-table-column label='操作' width='150'>
        <template slot-scope='scope'>
          <el-button type='text' @click='openDialog(scope.row)'>编辑</el-button>
          <el-button type='text' style='color:#f56c6c' @click='remove(scope.row.id)'>删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination :current-page.sync='query.page' :page-size='query.size' :total='total' layout='total, prev, pager, next' @current-change='load' style='margin-top: 15px;' />
    <el-dialog :title='form.id ? "编辑产品" : "新增产品"' :visible.sync='visible' width='500px'>
      <el-form :model='form' label-width='80px'>
        <el-form-item label='编码'><el-input v-model='form.code' /></el-form-item>
        <el-form-item label='名称'><el-input v-model='form.name' /></el-form-item>
        <el-form-item label='分类'><el-input v-model='form.category' /></el-form-item>
        <el-form-item label='价格'><el-input v-model='form.price' /></el-form-item>
        <el-form-item label='库存'><el-input v-model='form.stock' /></el-form-item>
        <el-form-item label='单位'><el-input v-model='form.unit' /></el-form-item>
      </el-form>
      <div slot='footer'><el-button @click='visible=false'>取消</el-button><el-button type='primary' @click='submit'>确定</el-button></div>
    </el-dialog>
  </div>
</template>

<script>
import { getProductList, createProduct, updateProduct, deleteProduct } from '@/api/product'
export default {
  data() { return { loading: false, list: [], total: 0, visible: false, query: { keyword: '', page: 1, size: 10 }, form: {} } },
  created() { this.load() },
  methods: {
    async load() { this.loading = true; const res = await getProductList(this.query); this.list = res.list; this.total = res.total; this.loading = false },
    openDialog(row = {}) { this.form = { ...row }; this.visible = true },
    async submit() { if (this.form.id) await updateProduct(this.form.id, this.form); else await createProduct(this.form); this.$message.success('操作成功'); this.visible = false; this.load() },
    async remove(id) { await this.$confirm('确认删除?', '提示', { type: 'warning' }); await deleteProduct(id); this.$message.success('删除成功'); this.load() }
  }
}
</script>
