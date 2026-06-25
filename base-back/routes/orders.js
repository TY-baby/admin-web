const express = require('express')
const router = express.Router()
const { authMiddleware } = require('../controllers/authController')
const ctrl = require('../controllers/orderController')

router.use(authMiddleware)
router.get('/', ctrl.list)
router.post('/', ctrl.create)
router.put('/:id', ctrl.update)
router.delete('/:id', ctrl.remove)

module.exports = router
