const { query } = require('../models/db')

function buildWhere(filters) {
  let where = 'WHERE 1=1'
  const params = []
  for (const key in filters) {
    if (filters[key] !== undefined && filters[key] !== '' && filters[key] !== null) {
      where += ` AND ${key} = ?`
      params.push(filters[key])
    }
  }
  return { where, params }
}

function createCrud(table, fields, searchFields = []) {
  return {
    async list(req, res) {
      const { keyword = '', page = 1, size = 10, ...filters } = req.query
      const limit = Number(size)
      const offset = (Number(page) - 1) * limit
      let { where, params } = buildWhere(filters)

      if (keyword && searchFields.length) {
        where += ' AND (' + searchFields.map(f => `${f} LIKE ?`).join(' OR ') + ')'
        const k = '%' + keyword + '%'
        searchFields.forEach(() => params.push(k))
      }

      const countRows = await query(`SELECT COUNT(*) AS total FROM ${table} ${where}`, params)
      const list = await query(`SELECT * FROM ${table} ${where} ORDER BY id DESC LIMIT ? OFFSET ?`, [...params, limit, offset])
      res.json({ code: 0, data: { list, total: countRows[0].total }, message: 'ok' })
    },

    async create(req, res) {
      const data = {}
      fields.forEach(f => { if (req.body[f] !== undefined) data[f] = req.body[f] })
      const cols = Object.keys(data)
      const vals = Object.values(data)
      const result = await query(`INSERT INTO ${table} (${cols.join(',')}) VALUES (${cols.map(() => '?').join(',')})`, vals)
      res.json({ code: 0, data: { id: result.insertId, ...data }, message: '新增成功' })
    },

    async update(req, res) {
      const id = Number(req.params.id)
      const data = {}
      fields.forEach(f => { if (req.body[f] !== undefined) data[f] = req.body[f] })
      const cols = Object.keys(data)
      const vals = Object.values(data)
      if (!cols.length) return res.json({ code: 0, message: '无更新' })
      await query(`UPDATE ${table} SET ${cols.map(c => `${c} = ?`).join(',')} WHERE id = ?`, [...vals, id])
      res.json({ code: 0, message: '更新成功' })
    },

    async remove(req, res) {
      const id = Number(req.params.id)
      await query(`DELETE FROM ${table} WHERE id = ?`, [id])
      res.json({ code: 0, message: '删除成功' })
    },

    async detail(req, res) {
      const id = Number(req.params.id)
      const rows = await query(`SELECT * FROM ${table} WHERE id = ?`, [id])
      res.json({ code: 0, data: rows[0] || null, message: 'ok' })
    }
  }
}

module.exports = { createCrud, buildWhere }
