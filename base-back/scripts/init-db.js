const { initTable } = require('../models/db')

initTable()
  .then(() => {
    console.log('数据库初始化完成')
    process.exit(0)
  })
  .catch(err => {
    console.error('数据库初始化失败:', err.message)
    process.exit(1)
  })
