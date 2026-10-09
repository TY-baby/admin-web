import request from './request'
export const listWithdraws = params => request({ url: '/admin/withdraw/list', method: 'get', params })
export const withdrawExportUrl = '/api/v1/admin/withdraw/export'
