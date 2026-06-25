<template>
  <div>
    <el-tabs v-model='activeName'>
      <el-tab-pane label='会员管理' name='member'>
        <el-form :inline='true' size='small'>
          <el-form-item label='关键字'><el-input v-model='query.keyword' clearable /></el-form-item>
          <el-form-item><el-button type='primary' @click='load'>查询</el-button></el-form-item>
        </el-form>
        <el-table :data='list' v-loading='loading' border>
          <el-table-column prop='customer_name' label='客户' />
          <el-table-column prop='vip_level_name' label='等级' />
          <el-table-column prop='points' label='积分' />
          <el-table-column prop='total_consumption' label='累计消费' />
          <el-table-column prop='expire_date' label='到期日' />
          <el-table-column label='操作' width='120'><template slot-scope='scope'><el-button type='text' @click='openPoints(scope.row)'>积分</el-button></template></el-table-column>
        </el-table>
        <el-pagination :current-page.sync='query.page' :page-size='query.size' :total='total' layout='total, prev, pager, next' @current-change='load' style='margin-top: 15px;' />
      </el-tab-pane>
      <el-tab-pane label='等级设置' name='level'>
        <el-button type='success' size='small' @click='openLevelDialog()'>新增等级</el-button>
        <el-table :data='levels' border style='margin-top: 15px;'>
          <el-table-column prop='name' label='等级名称' />
          <el-table-column prop='discount' label='折扣' />
          <el-table-column prop='threshold' label='门槛' />
          <el-table-column prop='privileges' label='权益' />
          <el-table-column label='操作' width='150'>
            <template slot-scope='scope'>
              <el-button type='text' @click='openLevelDialog(scope.row)'>编辑</el-button>
              <el-button type='text' style='color:#f56c6c' @click='removeLevel(scope.row.id)'>删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
    <el-dialog title='积分变动' :visible.sync='pointsVisible' width='400px'>
      <el-form :model='pointsForm' label-width='80px'>
        <el-form-item label='类型'>
          <el-select v-model='pointsForm.type'><el-option label='增加' value='add' /><el-option label='消费' value='minus' /></el-select>
        </el-form-item>
        <el-form-item label='积分'><el-input v-model='pointsForm.points' /></el-form-item>
        <el-form-item label='说明'><el-input v-model='pointsForm.description' type='textarea' /></el-form-item>
      </el-form>
      <div slot='footer'><el-button @click='pointsVisible=false'>取消</el-button><el-button type='primary' @click='submitPoints'>确定</el-button></div>
    </el-dialog>
    <el-dialog :title='levelForm.id ? "编辑等级" : "新增等级"' :visible.sync='levelVisible' width='500px'>
      <el-form :model='levelForm' label-width='80px'>
        <el-form-item label='名称'><el-input v-model='levelForm.name' /></el-form-item>
        <el-form-item label='等级值'><el-input v-model='levelForm.level' /></el-form-item>
        <el-form-item label='折扣'><el-input v-model='levelForm.discount' /></el-form-item>
        <el-form-item label='门槛'><el-input v-model='levelForm.threshold' /></el-form-item>
        <el-form-item label='权益'><el-input v-model='levelForm.privileges' type='textarea' /></el-form-item>
      </el-form>
      <div slot='footer'><el-button @click='levelVisible=false'>取消</el-button><el-button type='primary' @click='submitLevel'>确定</el-button></div>
    </el-dialog>
  </div>
</template>

<script>
import { getVipList, getVipLevels, createVipLevel, updateVipLevel, deleteVipLevel, addPoints } from '@/api/vip'
export default {
  data() {
    return { activeName: 'member', loading: false, list: [], total: 0, levels: [], query: { keyword: '', page: 1, size: 10 }, pointsVisible: false, pointsForm: {}, levelVisible: false, levelForm: {} }
  },
  created() { this.load(); this.loadLevels() },
  methods: {
    async load() { this.loading = true; const res = await getVipList(this.query); this.list = res.list; this.total = res.total; this.loading = false },
    async loadLevels() { this.levels = await getVipLevels() },
    openPoints(row) { this.pointsForm = { customer_id: row.customer_id, type: 'add', points: 0, description: '' }; this.pointsVisible = true },
    async submitPoints() { await addPoints(this.pointsForm); this.$message.success('积分变动成功'); this.pointsVisible = false; this.load() },
    openLevelDialog(row = {}) { this.levelForm = { ...row }; this.levelVisible = true },
    async submitLevel() { if (this.levelForm.id) await updateVipLevel(this.levelForm.id, this.levelForm); else await createVipLevel(this.levelForm); this.$message.success('操作成功'); this.levelVisible = false; this.loadLevels() },
    async removeLevel(id) { await this.$confirm('确认删除?', '提示', { type: 'warning' }); await deleteVipLevel(id); this.$message.success('删除成功'); this.loadLevels() }
  }
}
</script>
