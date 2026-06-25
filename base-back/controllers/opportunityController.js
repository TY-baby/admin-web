const { query } = require('../models/db')
const { createCrud } = require('./crudHelper')

const crud = createCrud('opportunities', 
  ['customer_id','title','amount','stage','probability','expected_close_date','owner_id','source','competitor','status','remark'],
  ['title']
)

exports.list = async (req, res) => {
  const { keyword = '', page = 1, size = 10, stage = '' } = req.query
  const limit = Number(size)
  const offset = (Number(page) - 1) * limit
  let where = 'WHERE 1=1'
  const params = []
  if (stage) { where += ' AND o.stage = ?'; params.push(stage) }
  if (keyword) { where += ' AND (o.title LIKE ? OR c.name LIKE ?)'; params.push('%' + keyword + '%', '%' + keyword + '%') }

  const countRows = await query(`SELECT COUNT(*) AS total FROM opportunities o LEFT JOIN customers c ON o.customer_id = c.id ${where}`, params)
  const list = await query(`
    SELECT o.*, c.name AS customer_name, c.company AS customer_company
    FROM opportunities o LEFT JOIN customers c ON o.customer_id = c.id
    ${where} ORDER BY o.id DESC LIMIT ? OFFSET ?`, [...params, limit, offset])

  res.json({ code: 0, data: { list, total: countRows[0].total }, message: 'ok' })
}

exports.create = crud.create
exports.update = crud.update
exports.remove = crud.remove

exports.follows = {
  async list(req, res) {
    const list = await query('SELECT * FROM opportunity_follows WHERE opportunity_id = ? ORDER BY id DESC', [Number(req.params.id)])
    res.json({ code: 0, data: list, message: 'ok' })
  },
  async create(req, res) {
    const { opportunity_id, follow_type, content, stage, owner_id } = req.body
    await query('INSERT INTO opportunity_follows (opportunity_id,follow_type,content,stage,owner_id) VALUES (?,?,?,?,?)',
      [opportunity_id, follow_type, content, stage, owner_id])
    await query('UPDATE opportunities SET stage = ? WHERE id = ?', [stage, opportunity_id])
    res.json({ code: 0, message: '跟进成功' })
  }
}
