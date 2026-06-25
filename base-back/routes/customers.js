const express = require('express')
const router = express.Router()
const { authMiddleware } = require('../controllers/authController')
const ctrl = require('../controllers/customerController')

router.use(authMiddleware)
router.get('/', ctrl.list)
router.post('/', ctrl.create)
router.put('/:id', ctrl.update)
router.delete('/:id', ctrl.remove)
router.get('/:id', ctrl.detail)
router.get('/:customerId/contacts', ctrl.contacts.list)
router.post('/contacts', ctrl.contacts.create)

module.exports = router
