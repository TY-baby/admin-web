import { post } from '../utils/request'

export const login = data => post('/auth/login', data)
export const logout = () => post('/auth/logout')
