const { createCrud } = require('./crudHelper')
const crud = createCrud('products', ['code','name','category','price','cost','stock','unit','status','remark'], ['name','code'])
exports.list = crud.list
exports.create = crud.create
exports.update = crud.update
exports.remove = crud.remove
exports.detail = crud.detail
