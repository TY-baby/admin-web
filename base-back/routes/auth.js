const express = require('express')
const router = express.Router()
const { login, logout, info, authMiddleware } = require('../controllers/authController')

router.post('/login', login)
router.get('/info', authMiddleware, info)
router.post('/logout', authMiddleware, logout)

module.exports = router
