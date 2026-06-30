import request from '../request'

// 图片检测
export const uploadImage = data => request.post('/plate/image/upload', data)
export const detectImage = data => request.post('/plate/image/detect', data)
export const batchDetectImage = data => request.post('/plate/image/batch-detect', data)
export const getImageList = params => request.get('/plate/image/list', { params })
export const getImageDetail = id => request.get('/plate/image/' + id + '/detail')
export const deleteImage = id => request.delete('/plate/image/' + id)
export const deleteImageBatch = data => request.post('/plate/image/batch-delete', data)

// 视频检测
export const uploadVideo = data => request.post('/plate/video/upload', data)
export const detectVideo = data => request.post('/plate/video/detect', data)
export const batchDetectVideo = data => request.post('/plate/video/batch-detect', data)
export const getVideoList = params => request.get('/plate/video/list', { params })
export const getVideoDetail = id => request.get('/plate/video/' + id + '/detail')
export const deleteVideo = id => request.delete('/plate/video/' + id)
export const deleteVideoBatch = data => request.post('/plate/video/batch-delete', data)

// 资源管理
export const getImageResourceList = params => request.get('/plate/resource/image', { params })
export const getVideoResourceList = params => request.get('/plate/resource/video', { params })
export const downloadImage = id => request.get('/plate/resource/image/' + id + '/download', { responseType: 'blob' })
export const downloadVideo = id => request.get('/plate/resource/video/' + id + '/download', { responseType: 'blob' })

// 系统日志
export const getLogList = params => request.get('/plate/logs', { params })
export const previewLog = params => request.get('/plate/logs/preview', { params })
export const downloadLog = name => request.get('/plate/logs/' + name + '/download', { responseType: 'blob' })
export const deleteLog = name => request.delete('/plate/logs/' + name)

// 数据可视化
export const getDashboardStats = () => request.get('/plate/dashboard/stats')
export const getRecentRecords = params => request.get('/plate/dashboard/recent', { params })

// 系统监控
export const getSystemMonitor = () => request.get('/plate/system/monitor')

// 模型管理
export const getModelList = params => request.get('/plate/models', { params })
export const uploadModel = data => request.post('/plate/models/upload', data)
export const updateModel = (id, data) => request.put('/plate/models/' + id, data)
export const loadModel = id => request.post('/plate/models/' + id + '/load')
export const deleteModel = id => request.delete('/plate/models/' + id)

// 大模型聊天
export const getTextModels = () => request.get('/plate/llm/models')
export const chatText = data => request.post('/plate/llm/chat', data)
export const chatTextStream = data => request.post('/plate/llm/chat-stream', data)

// 多模态聊天
export const getVisionModels = () => request.get('/plate/vision/models')
export const chatVision = data => request.post('/plate/vision/chat', data)
export const chatVisionStream = data => request.post('/plate/vision/chat-stream', data)

// 项目文档
export const getProjectDocs = () => request.get('/plate/docs')
