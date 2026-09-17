import request from './request'
export const login = data => request({ url: '/client/auth/login', method: 'post', data })