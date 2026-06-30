// H5 使用相对路径，开发时走 manifest.json 代理，生产时走 Nginx 代理
const BASE_URL = '/api'
const tokenKey = 'base_token'

function request(options) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync(tokenKey)
    uni.request({
      url: BASE_URL + options.url,
      method: options.method || 'GET',
      data: options.data || {},
      header: { Authorization: token ? 'Bearer ' + token : '' },
      success: res => {
        if (res.statusCode === 200 && res.data.code === 0) resolve(res.data.data)
        else {
          uni.showToast({ title: res.data.message || '请求失败', icon: 'none' })
          reject(res.data)
        }
      },
      fail: err => {
        uni.showToast({ title: '网络错误', icon: 'none' })
        reject(err)
      }
    })
  })
}

request.get = (url, params) => request({ url, method: 'GET', data: params && params.params })
request.post = (url, data) => request({ url, method: 'POST', data })
request.put = (url, data) => request({ url, method: 'PUT', data })
request.delete = url => request({ url, method: 'DELETE' })

export default request
