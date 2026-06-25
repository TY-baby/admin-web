<template>
  <div>
    <el-form :inline='true' size='small'>
      <el-form-item label='客户ID'><el-input v-model='query.customer_id' clearable /></el-form-item>
      <el-form-item><el-button type='primary' @click='load'>查询</el-button></el-form-item>
      <el-form-item><el-button type='success' @click='openDialog()'>新增跟进</el-button></el-form-item>
    </el-form>
    <el-table :data='list' v-loading='loading' border>
      <el-table-column prop='customer_name' label='客户' />
      <el-table-column prop='follow_type' label='跟进方式' />
      <el-table-column prop='content' label='内容' show-overflow-tooltip />
      <el-table-column prop='next_follow_time' label='下次跟进' />
      <el-table-column prop='create_time' label='记录时间' />
      <el-table-column label='操作' width='120'><template slot-scope='scope'><el-button type='text' style='color:#f56c6c' @click='remove(scope.row.id)'>删除</el-button></template></el-table-column>
    </el-table>
    <el-pagination :current-page.sync='query.page' :page-size='query.size' :total='total' layout='total, prev, pager, next' @current-change='load' style='margin-top: 15px;' />
    <el-dialog title='新增跟进' :visible.sync='visible' width='500px'>
      <el-form :model='form' label-width='80px'>
        <el-form-item label='客户ID'><el-input v-model='form.customer_id' /></el-form-item>
        <el-form-item label='跟进方式'>
          <el-select v-model='form.follow_type'><el-option label='电话' value='电话' /><el-option label='拜访' value='拜访' /><el-option label='邮件' value='邮件' /><el-option label='微信' value='微信' /></el-select>
        </el-form-item>
        <el-form-item label='内容'><el-input v-model='form.content' type='textarea' /></el-form-item>
        <el-form-item label='下次跟进'><el-date-picker v-model='form.next_follow_time' value-format='yyyy-MM-dd HH:mm:ss' /></el-form-item>
      </el-form>
      <div slot='footer'><el-button @click='visible=false'>取消</el-button><el-button type='primary' @click='submit'>确定</el-button></div>
    </el-dialog>
  </div>
</template>

<script>
import { getFollowList, createFollow, deleteFollow } from '@/api/follow'
export default {
  data() { return { loading: false, list: [], total: 0, visible: false, query: { customer_id: '', page: 1, size: 10 }, form: {} } },
  created() { this.load() },
  methods: {
    async load() { this.loading = true; const res = await getFollowList(this.query); this.list = res.list; this.total = res.total; this.loading = false },
    openDialog() { this.form = { follow_type: '电话' }; this.visible = true },
    async submit() { await createFollow(this.form); this.$message.success('新增成功'); this.visible = false; this.load() },
    async remove(id) { await this.$confirm('确认删除?', '提示', { type: 'warning' }); await deleteFollow(id); this.$message.success('删除成功'); this.load() }
  }
}
</script>
