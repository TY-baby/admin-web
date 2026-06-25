import request from './request'
export const getCustomerList = params => request.get('/customers', { params })
export const createCustomer = data => request.post('/customers', data)
export const getStats = () => request.get('/dashboard/stats')
export const getOpportunityList = params => request.get('/opportunities', { params })
export const getOrderList = params => request.get('/orders', { params })
