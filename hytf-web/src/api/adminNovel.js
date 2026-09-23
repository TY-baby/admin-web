import request from './request'
export const listNovel = params => request({ url: '/admin/novel/list', method: 'get', params })