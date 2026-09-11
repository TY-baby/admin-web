import axios from 'axios'

const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API || '/api',
  timeout: 10000
})

service.interceptors.response.use(
  response => response.data,
  error => Promise.reject(error)
)

export default service