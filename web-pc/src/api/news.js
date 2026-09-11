import request from './request'

export const getNewsList = () => request.get('/news').then(r => (r.data && r.data.list) || [])
export const getNewsDetail = id => request.get('/news/' + id).then(r => r.data)
export const recordClick = data => request.post('/click', data)