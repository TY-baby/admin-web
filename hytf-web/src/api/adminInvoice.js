import request from './request'
export const listInvoices = params => request({ url: '/admin/invoice/list', method: 'get', params })
export const createInvoice = data => request({ url: '/admin/invoice/create', method: 'post', data })
export const processInvoice = id => request({ url: '/admin/invoice/' + id + '/process', method: 'post' })