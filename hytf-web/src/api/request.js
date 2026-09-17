import axios from 'axios'
import { Message, MessageBox } from 'element-ui'
import { getClientToken, getAdminToken, removeClientToken, removeAdminToken } from '@/utils/auth'

const service = axios.create({
  baseURL: (process.env.VUE_APP_API_BASE || '') + '/api/v1',
  timeout: 15000
})

service.interceptors.request.use(config => {
  const isAdminApi = config.url && config.url.indexOf('/admin/') === 0
  const token = isAdminApi ? getAdminToken() : getClientToken()
  if (token) config.headers['Authorization'] = 'Bearer ' + token
  return config
}, err => Promise.reject(err))

service.interceptors.response.use(resp => {
  const body = resp.data
  if (body && typeof body === 'object' && 'code' in body && body.code !== 0) {
    Message.error(body.msg || '请求失败')
    return Promise.reject(new Error(body.msg || 'Error'))
  }
  return resp
}, err => {
  const status = err.response && err.response.status
  if (status === 401) {
    const isAdmin = err.config && err.config.url && err.config.url.indexOf('/admin/') === 0
    if (isAdmin) removeAdminToken(); else removeClientToken()
    MessageBox.alert('登录已过期，请重新登录', '提示', { type: 'warning' }).catch(() => {}).then(() => {
      window.location.hash = isAdmin ? '#/admin/login' : '#/client/login'
    })
  } else if (status === 429) {
    Message.warning('操作过于频繁，请稍后再试')
  } else {
    Message.error((err.response && err.response.data && err.response.data.msg) || err.message || '网络异常')
  }
  return Promise.reject(err)
})

export default service