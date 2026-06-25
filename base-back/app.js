const express = require('express')
const cors = require('cors')
const { initTable } = require('./models/db')
const config = require('./config')

const app = express()
app.use(cors())
app.use(express.json())

async function start() {
  await initTable()

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

  app.use((err, req, res, next) => {
    console.error(err.stack)
    res.status(500).json({ code: 1, message: err.message || '服务器内部错误' })
  })

  app.listen(config.port, () => {
    console.log('Server running on http://localhost:' + config.port)
  })
}

start().catch(err => {
  console.error('启动失败:', err)
  process.exit(1)
})
