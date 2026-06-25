const express = require('express')
const router = express.Router()
const { authMiddleware } = require('../controllers/authController')
const { stats } = require('../controllers/dashboardController')

router.use(authMiddleware)
router.get('/stats', stats)

module.exports = router
