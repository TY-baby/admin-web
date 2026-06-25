const express = require('express')
const router = express.Router()
const { authMiddleware } = require('../controllers/authController')
const ctrl = require('../controllers/vipController')

router.use(authMiddleware)
router.get('/levels', ctrl.levels.list)
router.post('/levels', ctrl.levels.create)
router.put('/levels/:id', ctrl.levels.update)
router.delete('/levels/:id', ctrl.levels.remove)
router.get('/', ctrl.list)
router.get('/points/:customerId', ctrl.points.list)
router.post('/points', ctrl.points.create)

module.exports = router
