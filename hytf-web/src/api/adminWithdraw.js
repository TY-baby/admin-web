import request from './request'
export const listWithdraws = params => request({ url: '/admin/withdraw/list', method: 'get', params })
export const listPayees = () => request({ url: '/admin/withdraw/payees', method: 'get' })
export const listWithdrawCustomers = params => request({ url: '/admin/withdraw/customers', method: 'get', params })
export const previewWithdraw = accountId => request({ url: '/admin/withdraw/preview/' + accountId, method: 'get' })
export const createWithdraw = data => request({ url: '/admin/withdraw/create', method: 'post', data })
export const deleteWithdraw = id => request({ url: '/admin/withdraw/' + id, method: 'delete' })
export const withdrawExportUrl = '/api/v1/admin/withdraw/export'
