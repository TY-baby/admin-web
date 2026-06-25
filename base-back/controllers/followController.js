const { query } = require('../models/db')
const { createCrud } = require('./crudHelper')

const crud = createCrud('follows', ['customer_id','follow_type','content','next_follow_time','owner_id'], ['content'])

exports.list = async (req, res) => {
  const { page = 1, size = 10, customer_id = '' } = req.query
  const limit = Number(size)
  const offset = (Number(page) - 1) * limit
  let where = 'WHERE 1=1'
  const params = []
  if (customer_id) { where += ' AND f.customer_id = ?'; params.push(customer_id) }
  const countRows = await query(`SELECT COUNT(*) AS total FROM follows f ${where}`, params)
  const list = await query(`
    SELECT f.*, c.name AS customer_name
    FROM follows f LEFT JOIN customers c ON f.customer_id = c.id
    ${where} ORDER BY f.id DESC LIMIT ? OFFSET ?`, [...params, limit, offset])
  res.json({ code: 0, data: { list, total: countRows[0].total }, message: 'ok' })
}
exports.create = crud.create
exports.update = crud.update
exports.remove = crud.remove
