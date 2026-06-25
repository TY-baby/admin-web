const express = require('express')
const cors = require('cors')
const config = require('./config')

const app = express()
app.use(cors())
app.use(express.json())

// Ensure all JSON responses use UTF-8 charset
app.use((req, res, next) => {
  res.setHeader('Content-Type', 'application/json; charset=utf-8')
  next()
})

// Health check endpoint - always available
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() })
})

// Register all routes immediately (routes don't depend on tables existing)
app.use('/api/auth', require('./routes/auth'))
app.use('/api/users', require('./routes/users'))
app.use('/api/dicts', require('./routes/dicts'))
app.use('/api/customers', require('./routes/customers'))
app.use('/api/opportunities', require('./routes/opportunities'))
app.use('/api/orders', require('./routes/orders'))
app.use('/api/follows', require('./routes/follows'))
app.use('/api/products', require('./routes/products'))
app.use('/api/vip', require('./routes/vip'))
app.use('/api/workflows', require('./routes/workflows'))
app.use('/api/dashboard', require('./routes/dashboard'))

app.get('/', (req, res) => res.json({ message: 'Base Room CRM API is running' }))

// Global error handler
app.use((err, req, res, next) => {
  console.error('[ERROR]', err.stack)
  res.status(500).json({ code: 1, message: err.message || '服务器内部错误' })
})

// START SERVER FIRST - never crash on startup
const server = app.listen(config.port, () => {
  console.log('[APP] Server running on http://localhost:' + config.port)
})

// Run database initialization in background (non-blocking)
const { initTable } = require('./models/db')
initTable()
  .then(() => {
    console.log('[APP] Database initialization completed successfully')
  })
  .catch(err => {
    // Log error but DON'T exit - server stays alive
    console.error('[APP] Database initialization failed (server still running):', err.message)
    console.error(err.stack)
  })

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('[APP] SIGTERM received, shutting down gracefully...')
  server.close(() => process.exit(0))
})
