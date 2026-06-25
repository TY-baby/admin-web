<template>
  <div>
    <el-tabs v-model='activeName'>
      <el-tab-pane label='流程定义' name='flow'>
        <el-button type='success' size='small' @click='openFlowDialog()'>新增流程</el-button>
        <el-table :data='flows' v-loading='loading' border style='margin-top: 15px;'>
          <el-table-column prop='name' label='流程名称' />
          <el-table-column prop='flow_key' label='编码' />
          <el-table-column prop='version' label='版本' />
          <el-table-column prop='status' label='状态' />
          <el-table-column label='操作' width='150'>
            <template slot-scope='scope'>
              <el-button type='text' @click='openFlowDialog(scope.row)'>编辑</el-button>
              <el-button type='text' style='color:#f56c6c' @click='removeFlow(scope.row.id)'>删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label='流程实例' name='instance'>
        <el-table :data='instances' border>
          <el-table-column prop='title' label='标题' />
          <el-table-column prop='workflow_name' label='流程' />
          <el-table-column prop='applicant_name' label='申请人' />
          <el-table-column prop='status' label='状态' />
          <el-table-column prop='current_node_id' label='当前节点' />
          <el-table-column label='操作' width='150'>
            <template slot-scope='scope'>
              <el-button type='text' @click='approve(scope.row.id, "approve")'>通过</el-button>
              <el-button type='text' style='color:#f56c6c' @click='approve(scope.row.id, "reject")'>驳回</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
    <el-dialog :title='flowForm.id ? "编辑流程" : "新增流程"' :visible.sync='flowVisible' width='600px'>
      <el-form :model='flowForm' label-width='80px'>
        <el-form-item label='名称'><el-input v-model='flowForm.name' /></el-form-item>
        <el-form-item label='编码'><el-input v-model='flowForm.flow_key' /></el-form-item>
        <el-form-item label='节点JSON'><el-input v-model='flowForm.nodesJson' type='textarea' :rows='5' /></el-form-item>
        <el-form-item label='备注'><el-input v-model='flowForm.remark' type='textarea' /></el-form-item>
      </el-form>
      <div slot='footer'><el-button @click='flowVisible=false'>取消</el-button><el-button type='primary' @click='submitFlow'>确定</el-button></div>
    </el-dialog>
  </div>
</template>

<script>
import { getWorkflowList, createWorkflow, updateWorkflow, deleteWorkflow, getInstanceList, approveInstance } from '@/api/workflow'
export default {
  data() { return { activeName: 'flow', loading: false, flows: [], instances: [], flowVisible: false, flowForm: {} } },
  created() { this.loadFlows(); this.loadInstances() },
  methods: {
    async loadFlows() { this.loading = true; this.flows = await getWorkflowList(); this.loading = false },
    async loadInstances() { this.instances = await getInstanceList() },
    openFlowDialog(row = {}) { this.flowForm = { ...row, nodesJson: row.nodes ? JSON.stringify(row.nodes) : '[]' }; this.flowVisible = true },
    async submitFlow() {
      const data = { name: this.flowForm.name, flow_key: this.flowForm.flow_key, remark: this.flowForm.remark, nodes: JSON.parse(this.flowForm.nodesJson) }
      if (this.flowForm.id) await updateWorkflow(this.flowForm.id, data); else await createWorkflow(data)
      this.$message.success('操作成功'); this.flowVisible = false; this.loadFlows()
    },
    async removeFlow(id) { await this.$confirm('确认删除?', '提示', { type: 'warning' }); await deleteWorkflow(id); this.$message.success('删除成功'); this.loadFlows() },
    async approve(id, action) { await approveInstance(id, { action, approver_id: 1, comment: '' }); this.$message.success('审批完成'); this.loadInstances() }
  }
}
</script>
