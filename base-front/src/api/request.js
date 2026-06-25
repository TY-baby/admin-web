import axios from 'axios'
import { Message } from 'element-ui'

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API || '/api',
  timeout: 10000
})

service.interceptors.request.use(config => {
  const token = localStorage.getItem('base_token')
  if (token) config.headers.Authorization = 'Bearer ' + token
  return config
})

service.interceptors.response.use(response => {
  const res = response.data
  if (res.code !== 0) {
    Message.error(res.message || '请求失败')
    return Promise.reject(new Error(res.message))
  }
  return res.data
}, error => {
  Message.error(error.response?.data?.message || '网络错误')
  return Promise.reject(error)
})

export default service
