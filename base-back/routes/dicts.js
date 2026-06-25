const express = require('express')
const router = express.Router()
const { authMiddleware } = require('../controllers/authController')
const ctrl = require('../controllers/dictController')

router.use(authMiddleware)
router.get('/', ctrl.list)
router.get('/all', ctrl.all)

module.exports = router
