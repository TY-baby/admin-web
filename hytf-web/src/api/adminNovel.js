import request from './request'
export const listNovel = params => request({ url: '/admin/novel/list', method: 'get', params })
export const novelExportUrl = '/api/v1/admin/customer/export'
