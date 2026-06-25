import request from './request'
export const getFollowList = params => request.get('/follows', { params })
export const createFollow = data => request.post('/follows', data)
export const updateFollow = (id, data) => request.put('/follows/' + id, data)
export const deleteFollow = id => request.delete('/follows/' + id)
