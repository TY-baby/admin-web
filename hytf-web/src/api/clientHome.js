import request from './request'
export const getAccounts = () => request({ url: '/client/home/accounts', method: 'get' })
export const getSummary = () => request({ url: '/client/home/summary', method: 'get' })
export const getTrend = params => request({ url: '/client/home/trend', method: 'get', params })