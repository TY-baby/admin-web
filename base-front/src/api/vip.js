import request from './request'
export const getVipList = params => request.get('/vip', { params })
export const getVipLevels = () => request.get('/vip/levels')
export const createVipLevel = data => request.post('/vip/levels', data)
export const updateVipLevel = (id, data) => request.put('/vip/levels/' + id, data)
export const deleteVipLevel = id => request.delete('/vip/levels/' + id)
export const getPoints = customerId => request.get('/vip/points/' + customerId)
export const addPoints = data => request.post('/vip/points', data)
