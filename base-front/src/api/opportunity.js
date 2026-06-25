import request from './request'
export const getOpportunityList = params => request.get('/opportunities', { params })
export const createOpportunity = data => request.post('/opportunities', data)
export const updateOpportunity = (id, data) => request.put('/opportunities/' + id, data)
export const deleteOpportunity = id => request.delete('/opportunities/' + id)
export const getOppFollows = id => request.get('/opportunities/' + id + '/follows')
export const addOppFollow = data => request.post('/opportunities/follows', data)
