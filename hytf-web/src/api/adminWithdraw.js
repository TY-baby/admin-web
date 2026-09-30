import request from './request'
export const listWithdraws = params => request({ url: '/admin/withdraw/list', method: 'get', params })
export const createWithdraw = data => request({ url: '/admin/withdraw/create', method: 'post', data })
export const deleteWithdraw = id => request({ url: '/admin/withdraw/' + id, method: 'delete' })