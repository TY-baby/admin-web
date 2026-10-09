import request from './request'
export const listLogs = params => request({ url: '/admin/system/log/list', method: 'get', params })
export const getMonitor = () => request({ url: '/admin/system/monitor/stats', method: 'get' })
export const listAccounts = () => request({ url: '/admin/system/account/list', method: 'get' })
export const getAccountMenus = () => request({ url: '/admin/system/account/menus', method: 'get' })
export const createAccount = data => request({ url: '/admin/system/account/create', method: 'post', data })
export const updateAccount = (id, data) => request({ url: '/admin/system/account/' + id, method: 'put', data })