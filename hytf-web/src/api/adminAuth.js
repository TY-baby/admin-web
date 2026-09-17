import request from './request'
export const login = data => request({ url: '/admin/auth/login', method: 'post', data })