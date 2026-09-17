import request from './request'
export const listCustomers = params => request({ url: '/admin/customer/list', method: 'get', params })
export const createCustomer = data => request({ url: '/admin/customer/create', method: 'post', data })
export const updateCustomer = (id, data) => request({ url: '/admin/customer/' + id, method: 'put', data })
export const updateDouyin = (id, data) => request({ url: '/admin/customer/douyin/' + id, method: 'put', data })
export const deleteCustomer = id => request({ url: '/admin/customer/' + id, method: 'delete' })
export const exportUrl = '/api/v1/admin/customer/export'