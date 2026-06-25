const { query } = require('../models/db')
const { createCrud } = require('./crudHelper')

const crud = createCrud('users', ['username','password','real_name','phone','email','avatar','dept_id','role_id','status'], ['username','real_name','phone'])

exports.list = async (req, res) => {
  const { keyword = '', page = 1, size = 10 } = req.query
  const limit = Number(size)
  const offset = (Number(page) - 1) * limit
  let where = 'WHERE 1=1'
  const params = []
  if (keyword) { where += ' AND (username LIKE ? OR real_name LIKE ? OR phone LIKE ?)'; params.push('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%') }
  const countRows = await query(`SELECT COUNT(*) AS total FROM users ${where}`, params)
  const list = await query(`SELECT id,username,real_name,phone,email,avatar,dept_id,role_id,status,create_time FROM users ${where} ORDER BY id DESC LIMIT ? OFFSET ?`, [...params, limit, offset])
  res.json({ code: 0, data: { list, total: countRows[0].total }, message: 'ok' })
}
exports.create = crud.create
exports.update = crud.update
exports.remove = crud.remove
exports.detail = crud.detail
