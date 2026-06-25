<template>
  <div>
    <el-form :inline='true' size='small'>
      <el-form-item label='关键字'><el-input v-model='query.keyword' clearable /></el-form-item>
      <el-form-item label='阶段'>
        <el-select v-model='query.stage' clearable>
          <el-option v-for='item in dicts.opportunity_stage' :key='item.id' :label='item.dict_label' :value='item.dict_value' />
        </el-select>
      </el-form-item>
      <el-form-item><el-button type='primary' @click='load'>查询</el-button></el-form-item>
      <el-form-item><el-button type='success' @click='openDialog()'>新增商机</el-button></el-form-item>
    </el-form>
    <el-table :data='list' v-loading='loading' border>
      <el-table-column prop='title' label='商机标题' />
      <el-table-column prop='customer_name' label='客户' />
      <el-table-column prop='amount' label='预计金额' />
      <el-table-column prop='stage' label='阶段' />
      <el-table-column prop='probability' label='赢单概率' />
      <el-table-column prop='expected_close_date' label='预计成交' />
      <el-table-column label='操作' width='200'>
        <template slot-scope='scope'>
          <el-button type='text' @click='openDialog(scope.row)'>编辑</el-button>
          <el-button type='text' @click='openFollow(scope.row)'>跟进</el-button>
          <el-button type='text' style='color:#f56c6c' @click='remove(scope.row.id)'>删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination :current-page.sync='query.page' :page-size='query.size' :total='total' layout='total, prev, pager, next' @current-change='load' style='margin-top: 15px;' />
    <el-dialog :title='form.id ? "编辑商机" : "新增商机"' :visible.sync='visible' width='600px'>
      <el-form :model='form' label-width='100px'>
        <el-form-item label='关联客户'><el-input v-model='form.customer_id' placeholder='客户ID' /></el-form-item>
        <el-form-item label='商机标题'><el-input v-model='form.title' /></el-form-item>
        <el-form-item label='预计金额'><el-input v-model='form.amount' /></el-form-item>
        <el-form-item label='阶段'>
          <el-select v-model='form.stage'>
            <el-option v-for='item in dicts.opportunity_stage' :key='item.id' :label='item.dict_label' :value='item.dict_value' />
          </el-select>
        </el-form-item>
        <el-form-item label='赢单概率'><el-input v-model='form.probability' /></el-form-item>
        <el-form-item label='预计成交'><el-date-picker v-model='form.expected_close_date' value-format='yyyy-MM-dd' /></el-form-item>
        <el-form-item label='备注'><el-input v-model='form.remark' type='textarea' /></el-form-item>
      </el-form>
      <div slot='footer'><el-button @click='visible=false'>取消</el-button><el-button type='primary' @click='submit'>确定</el-button></div>
    </el-dialog>
    <el-dialog title='跟进' :visible.sync='followVisible' width='500px'>
      <el-form :model='followForm' label-width='80px'>
        <el-form-item label='跟进方式'>
          <el-select v-model='followForm.follow_type'><el-option label='电话' value='电话' /><el-option label='拜访' value='拜访' /><el-option label='邮件' value='邮件' /></el-select>
        </el-form-item>
        <el-form-item label='阶段'><el-input v-model='followForm.stage' /></el-form-item>
        <el-form-item label='内容'><el-input v-model='followForm.content' type='textarea' /></el-form-item>
      </el-form>
      <div slot='footer'><el-button @click='followVisible=false'>取消</el-button><el-button type='primary' @click='submitFollow'>确定</el-button></div>
    </el-dialog>
  </div>
</template>

<script>
import { getOpportunityList, createOpportunity, updateOpportunity, deleteOpportunity, addOppFollow } from '@/api/opportunity'
import { getAllDicts } from '@/api/dashboard'
export default {
  data() {
    return { loading: false, list: [], total: 0, visible: false, followVisible: false, query: { keyword: '', stage: '', page: 1, size: 10 }, form: {}, followForm: {}, dicts: { opportunity_stage: [] } }
  },
  created() { this.loadDicts(); this.load() },
  methods: {
    async loadDicts() { this.dicts = await getAllDicts() },
    async load() { this.loading = true; const res = await getOpportunityList(this.query); this.list = res.list; this.total = res.total; this.loading = false },
    openDialog(row = {}) { this.form = { ...row }; this.visible = true },
    async submit() { if (this.form.id) await updateOpportunity(this.form.id, this.form); else await createOpportunity(this.form); this.$message.success('操作成功'); this.visible = false; this.load() },
    openFollow(row) { this.followForm = { opportunity_id: row.id, stage: row.stage, follow_type: '电话', content: '' }; this.followVisible = true },
    async submitFollow() { await addOppFollow(this.followForm); this.$message.success('跟进成功'); this.followVisible = false; this.load() },
    async remove(id) { await this.$confirm('确认删除?', '提示', { type: 'warning' }); await deleteOpportunity(id); this.$message.success('删除成功'); this.load() }
  }
}
</script>
