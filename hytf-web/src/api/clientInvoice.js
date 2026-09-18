import request from './request'
export const applyInvoice = data => request({ url: '/client/invoice/apply', method: 'post', data })
export const listMyInvoices = params => request({ url: '/client/invoice/list', method: 'get', params })
