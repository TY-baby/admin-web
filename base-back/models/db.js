const mysql = require('mysql2/promise')
const fs = require('fs')
const path = require('path')
const config = require('../config')

const pool = mysql.createPool(config.db)

async function query(sql, params) {
  const [rows] = await pool.query(sql, params)
  return rows
}

async function transaction(fn) {
  const connection = await pool.getConnection()
  await connection.beginTransaction()
  try {
    const result = await fn(connection)
    await connection.commit()
    return result
  } catch (err) {
    await connection.rollback()
    throw err
  } finally {
    connection.release()
  }
}

async function ensureDatabase() {
  // Connect without database to ensure database exists
  const dbConfig = { ...config.db }
  delete dbConfig.database
  const tempPool = mysql.createPool(dbConfig)
  try {
    await tempPool.query(`CREATE DATABASE IF NOT EXISTS \`${config.db.database}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`)
  } finally {
    await tempPool.end()
  }
}

async function initTable() {
  await ensureDatabase()

  const sql = fs.readFileSync(path.join(__dirname, 'init.sql'), 'utf8')
  const statements = sql.split(';').filter(s => {
    const t = s.trim()
    return t && !t.toUpperCase().startsWith('USE ') && !t.toUpperCase().startsWith('CREATE DATABASE')
  })

  // Run CREATE statements first
  const createStmts = statements.filter(s => !s.trim().toUpperCase().startsWith('INSERT'))
  for (const stmt of createStmts) {
    await query(stmt)
  }

  // Check if users table has data, skip seed inserts if already seeded
  let seeded = false
  try {
    const rows = await query('SELECT COUNT(*) AS total FROM users')
    seeded = rows[0].total > 0
  } catch (e) {}

  if (!seeded) {
    const insertStmts = statements.filter(s => s.trim().toUpperCase().startsWith('INSERT'))
    for (const stmt of insertStmts) {
      await query(stmt)
    }
  }
}

module.exports = { pool, query, transaction, initTable }
