import { get } from '../utils/request'

export const getStats = () => get('/dashboard/stats')
