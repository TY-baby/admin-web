const { query, transaction } = require('../models/db')

function genOrderNo() {
  const now = new Date()
  return 'O' + now.getFullYear() + String(now.getMonth()+1).padStart(2,'0') + String(now.getDate()).padStart(2,'0') + String(Math.floor(Math.random()*9000)+1000)
}

exports.list = async (req, res) => {
  const { keyword = '', page = 1, size = 10, status = '' } = req.query
  const limit = Number(size)
  const offset = (Number(page) - 1) * limit
  let where = 'WHERE 1=1'
  const params = []
  if (status) { where += ' AND o.status = ?'; params.push(status) }
  if (keyword) { where += ' AND (o.order_no LIKE ? OR c.name LIKE ?)'; params.push('%' + keyword + '%', '%' + keyword + '%') }

  const countRows = await query(`SELECT COUNT(*) AS total FROM orders o LEFT JOIN customers c ON o.customer_id = c.id ${where}`, params)
  const list = await query(`
    SELECT o.*, c.name AS customer_name
    FROM orders o LEFT JOIN customers c ON o.customer_id = c.id
    ${where} ORDER BY o.id DESC LIMIT ? OFFSET ?`, [...params, limit, offset])

  for (const order of list) {
    order.items = await query('SELECT * FROM order_items WHERE order_id = ?', [order.id])
  }
  res.json({ code: 0, data: { list, total: countRows[0].total }, message: 'ok' })
}

exports.create = async (req, res) => {
  const { customer_id, opportunity_id, amount, discount, actual_amount, status, pay_status, order_date, delivery_date, owner_id, remark, items = [] } = req.body
  const orderNo = genOrderNo()
  await transaction(async conn => {
    const [result] = await conn.execute(
      'INSERT INTO orders (order_no,customer_id,opportunity_id,amount,discount,actual_amount,status,pay_status,order_date,delivery_date,owner_id,remark) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
      [orderNo, customer_id, opportunity_id, amount, discount, actual_amount, status, pay_status, order_date, delivery_date, owner_id, remark]
    )
    for (const item of items) {
      await conn.execute('INSERT INTO order_items (order_id,product_id,product_name,quantity,unit_price,total_price) VALUES (?,?,?,?,?,?)',
        [result.insertId, item.product_id, item.product_name, item.quantity, item.unit_price, item.total_price])
    }
  })
  res.json({ code: 0, data: { order_no: orderNo }, message: '订单创建成功' })
}

exports.update = async (req, res) => {
  const id = Number(req.params.id)
  const fields = ['customer_id','opportunity_id','amount','discount','actual_amount','status','pay_status','order_date','delivery_date','owner_id','remark']
  const data = {}
  fields.forEach(f => { if (req.body[f] !== undefined) data[f] = req.body[f] })
  const cols = Object.keys(data)
  if (cols.length) {
    await query('UPDATE orders SET ' + cols.map(c => `${c} = ?`).join(',') + ' WHERE id = ?', [...Object.values(data), id])
  }
  res.json({ code: 0, message: '更新成功' })
}

exports.remove = async (req, res) => {
  const id = Number(req.params.id)
  await query('DELETE FROM order_items WHERE order_id = ?', [id])
  await query('DELETE FROM orders WHERE id = ?', [id])
  res.json({ code: 0, message: '删除成功' })
}
