const { query } = require('../models/db')

exports.list = async (req, res) => {
  const list = await query('SELECT id,name,flow_key,version,status,remark,create_time FROM workflows')
  res.json({ code: 0, data: list, message: 'ok' })
}

exports.create = async (req, res) => {
  const { name, flow_key, nodes, remark } = req.body
  const result = await query('INSERT INTO workflows (name,flow_key,nodes,remark) VALUES (?,?,?,?)', [name, flow_key, JSON.stringify(nodes), remark])
  res.json({ code: 0, data: { id: result.insertId }, message: '新增成功' })
}

exports.update = async (req, res) => {
  const id = Number(req.params.id)
  const { name, nodes, remark, status } = req.body
  await query('UPDATE workflows SET name=?,nodes=?,remark=?,status=? WHERE id=?', [name, JSON.stringify(nodes), remark, status, id])
  res.json({ code: 0, message: '更新成功' })
}

exports.remove = async (req, res) => {
  await query('DELETE FROM workflows WHERE id = ?', [Number(req.params.id)])
  res.json({ code: 0, message: '删除成功' })
}

exports.instances = {
  async list(req, res) {
    const list = await query(`
      SELECT wi.*, w.name AS workflow_name, u.real_name AS applicant_name
      FROM workflow_instances wi
      LEFT JOIN workflows w ON wi.workflow_id = w.id
      LEFT JOIN users u ON wi.applicant_id = u.id
      ORDER BY wi.id DESC`)
    res.json({ code: 0, data: list, message: 'ok' })
  },
  async create(req, res) {
    const { workflow_id, business_key, business_type, title, applicant_id } = req.body
    const [wf] = await query('SELECT nodes FROM workflows WHERE id = ?', [workflow_id])
    const nodes = JSON.parse(wf.nodes || '[]')
    const firstNode = nodes.find(n => n.nodeType === 'approval') || nodes[0]
    const result = await query('INSERT INTO workflow_instances (workflow_id,business_key,business_type,title,applicant_id,current_node_id) VALUES (?,?,?,?,?,?)',
      [workflow_id, business_key, business_type, title, applicant_id, firstNode ? firstNode.nodeId : ''])
    res.json({ code: 0, data: { id: result.insertId }, message: '流程发起成功' })
  },
  async approve(req, res) {
    const id = Number(req.params.id)
    const { action, comment, approver_id } = req.body
    const [instance] = await query('SELECT * FROM workflow_instances WHERE id = ?', [id])
    if (!instance) return res.json({ code: 1, message: '流程不存在' })

    await query('INSERT INTO workflow_approvals (instance_id,node_id,node_name,approver_id,action,comment) VALUES (?,?,?,?,?,?)',
      [id, instance.current_node_id, instance.current_node_id, approver_id, action, comment])

    if (action === 'reject') {
      await query('UPDATE workflow_instances SET status = ? WHERE id = ?', ['rejected', id])
    } else {
      const [wf] = await query('SELECT nodes FROM workflows WHERE id = ?', [instance.workflow_id])
      const nodes = JSON.parse(wf.nodes || '[]')
      const current = nodes.find(n => n.nodeId === instance.current_node_id)
      const nextId = current && current.nextNodes ? current.nextNodes : ''
      const nextNode = nodes.find(n => n.nodeId === nextId)
      if (!nextNode || nextNode.nodeType === 'end') {
        await query('UPDATE workflow_instances SET status = ?, current_node_id = ? WHERE id = ?', ['approved', 'end', id])
      } else {
        await query('UPDATE workflow_instances SET current_node_id = ? WHERE id = ?', [nextNode.nodeId, id])
      }
    }
    res.json({ code: 0, message: '审批完成' })
  }
}
