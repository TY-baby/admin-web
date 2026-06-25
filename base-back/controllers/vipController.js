const { query } = require('../models/db')

exports.levels = {
  async list(req, res) {
    const list = await query('SELECT * FROM vip_levels ORDER BY level ASC')
    res.json({ code: 0, data: list, message: 'ok' })
  },
  async create(req, res) {
    const { name, level, discount, threshold, privileges } = req.body
    const result = await query('INSERT INTO vip_levels (name,level,discount,threshold,privileges) VALUES (?,?,?,?,?)',
      [name, level, discount, threshold, privileges])
    res.json({ code: 0, data: { id: result.insertId }, message: '新增成功' })
  },
  async update(req, res) {
    const id = Number(req.params.id)
    const { name, level, discount, threshold, privileges, status } = req.body
    await query('UPDATE vip_levels SET name=?,level=?,discount=?,threshold=?,privileges=?,status=? WHERE id=?',
      [name, level, discount, threshold, privileges, status, id])
    res.json({ code: 0, message: '更新成功' })
  },
  async remove(req, res) {
    await query('DELETE FROM vip_levels WHERE id = ?', [Number(req.params.id)])
    res.json({ code: 0, message: '删除成功' })
  }
}

exports.list = async (req, res) => {
  const { keyword = '', page = 1, size = 10 } = req.query
  const limit = Number(size)
  const offset = (Number(page) - 1) * limit
  let where = 'WHERE 1=1'
  const params = []
  if (keyword) { where += ' AND (c.name LIKE ? OR c.phone LIKE ?)'; params.push('%' + keyword + '%', '%' + keyword + '%') }
  const countRows = await query(`SELECT COUNT(*) AS total FROM customer_vip cv LEFT JOIN customers c ON cv.customer_id = c.id ${where}`, params)
  const list = await query(`
    SELECT cv.*, c.name AS customer_name, c.phone AS customer_phone, vl.name AS vip_level_name
    FROM customer_vip cv
    LEFT JOIN customers c ON cv.customer_id = c.id
    LEFT JOIN vip_levels vl ON cv.vip_level_id = vl.id
    ${where} ORDER BY cv.total_consumption DESC LIMIT ? OFFSET ?`, [...params, limit, offset])
  res.json({ code: 0, data: { list, total: countRows[0].total }, message: 'ok' })
}

exports.points = {
  async list(req, res) {
    const list = await query('SELECT pr.*, c.name AS customer_name FROM points_records pr LEFT JOIN customers c ON pr.customer_id = c.id WHERE pr.customer_id = ? ORDER BY pr.id DESC', [Number(req.params.customerId)])
    res.json({ code: 0, data: list, message: 'ok' })
  },
  async create(req, res) {
    const { customer_id, type, points, description } = req.body
    const [row] = await query('SELECT points FROM customer_vip WHERE customer_id = ?', [customer_id])
    const balance = row ? (type === 'add' ? row.points + points : row.points - points) : points
    await query('INSERT INTO points_records (customer_id,type,points,balance,description) VALUES (?,?,?,?,?)',
      [customer_id, type, points, balance, description])
    await query('UPDATE customer_vip SET points = ? WHERE customer_id = ?', [balance, customer_id])
    res.json({ code: 0, message: '积分记录成功' })
  }
}
