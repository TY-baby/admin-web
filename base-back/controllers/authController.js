const jwt = require('jsonwebtoken')
const bcrypt = require('bcryptjs')
const { query } = require('../models/db')
const config = require('../config')

exports.login = async (req, res) => {
  const { username, password } = req.body
  const rows = await query('SELECT * FROM users WHERE username = ?', [username])
  const user = rows[0]
  if (!user) return res.status(401).json({ code: 1, message: '用户名或密码错误' })
  const isMatch = await bcrypt.compare(password, user.password)
  if (!isMatch) return res.status(401).json({ code: 1, message: '用户名或密码错误' })
  const token = jwt.sign({ userId: user.id, username: user.username, roleId: user.role_id }, config.jwtSecret, { expiresIn: config.expiresIn })
  res.json({
    code: 0,
    data: {
      token,
      userInfo: { id: user.id, username: user.username, real_name: user.real_name, role_id: user.role_id, dept_id: user.dept_id }
    },
    message: '登录成功'
  })
}

exports.info = async (req, res) => {
  const rows = await query('SELECT id, username, real_name, phone, email, avatar, dept_id, role_id, status FROM users WHERE id = ?', [req.user.userId])
  res.json({ code: 0, data: rows[0] || null, message: 'ok' })
}

exports.logout = (req, res) => {
  res.json({ code: 0, message: '退出成功' })
}

exports.authMiddleware = (req, res, next) => {
  const auth = req.headers.authorization
  if (!auth) return res.status(401).json({ code: 1, message: '缺少 token' })
  const token = auth.replace('Bearer ', '')
  try {
    req.user = jwt.verify(token, config.jwtSecret)
    next()
  } catch (e) {
    res.status(401).json({ code: 1, message: 'token 无效' })
  }
}
