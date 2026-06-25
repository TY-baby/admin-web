const { query } = require('../models/db')

exports.list = async (req, res) => {
  const { dict_type = '' } = req.query
  const list = await query('SELECT * FROM sys_dicts WHERE dict_type = ? ORDER BY sort ASC', [dict_type])
  res.json({ code: 0, data: list, message: 'ok' })
}

exports.all = async (req, res) => {
  const list = await query('SELECT * FROM sys_dicts ORDER BY dict_type, sort')
  const result = {}
  list.forEach(item => {
    if (!result[item.dict_type]) result[item.dict_type] = []
    result[item.dict_type].push(item)
  })
  res.json({ code: 0, data: result, message: 'ok' })
}
