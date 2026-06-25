import request from './request'
export const getOrderList = params => request.get('/orders', { params })
export const createOrder = data => request.post('/orders', data)
export const updateOrder = (id, data) => request.put('/orders/' + id, data)
export const deleteOrder = id => request.delete('/orders/' + id)
