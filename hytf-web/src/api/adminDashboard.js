import request from './request'
export const getOverview = params => request({ url: '/admin/dashboard/overview', method: 'get', params })