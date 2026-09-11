import request from './request'

export const getTransactions = params => request.get('/transactions', { params })