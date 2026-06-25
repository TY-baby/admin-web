const express = require('express')
const router = express.Router()
const { authMiddleware } = require('../controllers/authController')
const ctrl = require('../controllers/workflowController')

router.use(authMiddleware)
router.get('/', ctrl.list)
router.post('/', ctrl.create)
router.put('/:id', ctrl.update)
router.delete('/:id', ctrl.remove)
router.get('/instances', ctrl.instances.list)
router.post('/instances', ctrl.instances.create)
router.post('/instances/:id/approve', ctrl.instances.approve)

module.exports = router
