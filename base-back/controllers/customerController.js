const { query } = require('../models/db')
const { createCrud } = require('./crudHelper')

const crud = createCrud('customers', 
  ['customer_no','name','phone','email','company','industry','source','status','level','owner_id','province','city','district','address','tags','remark'],
  ['name','phone','company']
)

exports.list = crud.list
exports.create = crud.create
exports.update = crud.update
exports.remove = crud.remove
exports.detail = async (req, res) => {
  const id = Number(req.params.id)
  const [customer] = await query('SELECT * FROM customers WHERE id = ?', [id])
  if (!customer) return res.json({ code: 1, message: '客户不存在' })
  const contacts = await query('SELECT * FROM customer_contacts WHERE customer_id = ?', [id])
  const follows = await query('SELECT * FROM follows WHERE customer_id = ? ORDER BY id DESC LIMIT 10', [id])
  const opportunities = await query('SELECT * FROM opportunities WHERE customer_id = ? ORDER BY id DESC', [id])
  const orders = await query('SELECT * FROM orders WHERE customer_id = ? ORDER BY id DESC', [id])
  res.json({ code: 0, data: { ...customer, contacts, follows, opportunities, orders }, message: 'ok' })
}

exports.contacts = {
  async list(req, res) {
    const customerId = Number(req.params.customerId)
    const list = await query('SELECT * FROM customer_contacts WHERE customer_id = ?', [customerId])
    res.json({ code: 0, data: list, message: 'ok' })
  },
  async create(req, res) {
    const { customer_id, name, phone, email, position, is_main, remark } = req.body
    const result = await query('INSERT INTO customer_contacts (customer_id,name,phone,email,position,is_main,remark) VALUES (?,?,?,?,?,?,?)',
      [customer_id, name, phone, email, position, is_main, remark])
    res.json({ code: 0, data: { id: result.insertId }, message: '新增成功' })
  }
}
