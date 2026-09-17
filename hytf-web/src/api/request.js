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
    Message.error(body.msg || '璇锋眰澶辫触')
    return Promise.reject(new Error(body.msg || 'Error'))
  }
  return resp
}, err => {
  const status = err.response && err.response.status
  if (status === 401) {
    const isAdmin = err.config && err.config.url && err.config.url.indexOf('/admin/') === 0
    if (isAdmin) removeAdminToken(); else removeClientToken()
    MessageBox.alert('鐧诲綍宸茶繃鏈燂紝璇烽噸鏂扮櫥褰?, '鎻愮ず', { type: 'warning' }).catch(() => {}).then(() => {
      window.location.hash = isAdmin ? '#/admin/login' : '#/client/login'
    })
  } else if (status === 429) {
    Message.warning('鎿嶄綔杩囦簬棰戠箒锛岃绋嶅悗鍐嶈瘯')
  } else {
    Message.error((err.response && err.response.data && err.response.data.msg) || err.message || '缃戠粶寮傚父')
  }
  return Promise.reject(err)
})

export default service