const mysql = require('mysql2/promise')
const fs = require('fs')
const path = require('path')
const config = require('../config')

const pool = mysql.createPool({
  ...config.db,
  charset: 'utf8mb4'
})

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

function isValidStatement(s) {
  // Remove all comment lines, then check if there's real SQL
  const lines = s.split('\n').filter(l => !l.trim().startsWith('--'))
  const cleaned = lines.join('\n').trim()
  if (!cleaned) return false
  const upper = cleaned.toUpperCase()
  if (upper.startsWith('USE ')) return false
  if (upper.startsWith('CREATE DATABASE')) return false
  return true
}

async function ensureDatabase() {
  const dbConfig = { ...config.db, charset: 'utf8mb4' }
  delete dbConfig.database
  const tempPool = mysql.createPool(dbConfig)
  try {
    await tempPool.query(
      `CREATE DATABASE IF NOT EXISTS \`${config.db.database}\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`
    )
    console.log('[DB] Database ensured:', config.db.database)
  } catch (e) {
    // May fail if user lacks CREATE DATABASE privilege, but DB might already exist
    console.log('[DB] ensureDatabase warning (database may already exist):', e.message)
  } finally {
    await tempPool.end()
  }
}

async function initTable() {
  await ensureDatabase()

  const sql = fs.readFileSync(path.join(__dirname, 'init.sql'), 'utf8')
  const statements = sql.split(';').filter(isValidStatement)

  // Separate CREATE and INSERT statements
  const createStmts = []
  const insertStmts = []
  for (const stmt of statements) {
    const lines = stmt.split('\n').filter(l => !l.trim().startsWith('--'))
    const cleaned = lines.join('\n').trim()
    if (cleaned.toUpperCase().startsWith('INSERT')) {
      insertStmts.push(cleaned)
    } else {
      createStmts.push(cleaned)
    }
  }

  // Run CREATE TABLE statements with error tolerance
  console.log('[DB] Running', createStmts.length, 'CREATE statements...')
  for (const stmt of createStmts) {
    try {
      await query(stmt)
    } catch (e) {
      // Log but continue - table might already exist
      console.log('[DB] CREATE warning:', e.message.substring(0, 80))
    }
  }

  // Check if already seeded
  let seeded = false
  try {
    const rows = await query('SELECT COUNT(*) AS total FROM users')
    seeded = rows[0].total > 0
    console.log('[DB] Users count:', rows[0].total, seeded ? '(already seeded)' : '(will seed)')
  } catch (e) {
    console.log('[DB] Seed check error:', e.message)
  }

  if (!seeded) {
    console.log('[DB] Seeding', insertStmts.length, 'INSERT statements...')
    for (const stmt of insertStmts) {
      try {
        await query(stmt)
      } catch (e) {
        console.log('[DB] INSERT warning:', e.message.substring(0, 80))
      }
    }
  }

  console.log('[DB] Initialization complete')
}

module.exports = { pool, query, transaction, initTable }
