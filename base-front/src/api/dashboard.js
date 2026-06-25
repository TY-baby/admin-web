import request from './request'
export const getStats = () => request.get('/dashboard/stats')
export const getDicts = type => request.get('/dicts', { params: { dict_type: type } })
export const getAllDicts = () => request.get('/dicts/all')
