import request from './request'

export const login = data => request.post('/auth/login', data)
export const logout = () => request.post('/auth/logout')
