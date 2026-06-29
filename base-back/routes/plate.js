const express = require('express')
const router = express.Router()
const { authMiddleware } = require('../controllers/authController')
const ctrl = require('../controllers/plateController')

router.use(authMiddleware)

// 图片
router.post('/image/upload', ctrl.uploadImage, ctrl.imageUpload)
router.post('/image/detect', ctrl.imageDetect)
router.post('/image/batch-detect', ctrl.imageBatchDetect)
router.get('/image/list', ctrl.imageList)
router.delete('/image/:id', ctrl.imageDelete)
router.post('/image/batch-delete', ctrl.imageBatchDelete)

// 视频
router.post('/video/upload', ctrl.uploadVideo, ctrl.videoUpload)
router.post('/video/detect', ctrl.videoDetect)
router.post('/video/batch-detect', ctrl.videoBatchDetect)
router.get('/video/list', ctrl.videoList)
router.delete('/video/:id', ctrl.videoDelete)
router.post('/video/batch-delete', ctrl.videoBatchDelete)

// 资源管理
router.get('/resource/image', ctrl.imageResourceList)
router.get('/resource/video', ctrl.videoResourceList)
router.get('/resource/image/:id/download', ctrl.downloadImage)
router.get('/resource/video/:id/download', ctrl.downloadVideo)

// 日志
router.get('/logs', ctrl.logList)
router.get('/logs/preview', ctrl.logPreview)
router.get('/logs/:name/download', ctrl.logDownload)
router.delete('/logs/:name', ctrl.logDelete)

// 数据可视化
router.get('/dashboard/stats', ctrl.dashboardStats)
router.get('/dashboard/recent', ctrl.recentRecords)

// 系统监控
router.get('/system/monitor', ctrl.systemMonitor)

// 模型管理
router.get('/models', ctrl.modelList)
router.post('/models/upload', ctrl.uploadModel, ctrl.modelUpload)
router.put('/models/:id', ctrl.modelUpdate)
router.post('/models/:id/load', ctrl.modelLoad)
router.delete('/models/:id', ctrl.modelDelete)

// LLM
router.get('/llm/models', ctrl.textModels)
router.post('/llm/chat', ctrl.chatText)
router.post('/llm/chat-stream', ctrl.chatTextStream)

// 多模态
router.get('/vision/models', ctrl.visionModels)
router.post('/vision/chat', ctrl.chatVision)
router.post('/vision/chat-stream', ctrl.chatVisionStream)

// 文档
router.get('/docs', ctrl.projectDocs)

module.exports = router
