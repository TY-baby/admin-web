const fs = require('fs')
const path = require('path')
const os = require('os')
const multer = require('multer')
const { query } = require('../models/db')

const UPLOAD_DIR = path.join(__dirname, '..', 'uploads')
const IMAGE_DIR = path.join(UPLOAD_DIR, 'images')
const VIDEO_DIR = path.join(UPLOAD_DIR, 'videos')
const MODEL_DIR = path.join(UPLOAD_DIR, 'models')
const LOG_DIR = path.join(__dirname, '..', 'logs')

function ensureDirs() {
  [UPLOAD_DIR, IMAGE_DIR, VIDEO_DIR, MODEL_DIR, LOG_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true })
  })
}
ensureDirs()

function decodeFilename(filename) {
  // multer/busboy 默认把 UTF-8 文件名按 latin1 解码，需要转回来
  return Buffer.from(filename, 'latin1').toString('utf8')
}

const imageStorage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, IMAGE_DIR),
  filename: (req, file, cb) => {
    const unique = Date.now() + '-' + Math.round(Math.random() * 1e9)
    cb(null, unique + path.extname(file.originalname))
  }
})

const videoStorage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, VIDEO_DIR),
  filename: (req, file, cb) => {
    const unique = Date.now() + '-' + Math.round(Math.random() * 1e9)
    cb(null, unique + path.extname(file.originalname))
  }
})

const modelStorage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, MODEL_DIR),
  filename: (req, file, cb) => cb(null, decodeFilename(file.originalname))
})

exports.uploadImage = multer({ storage: imageStorage, limits: { fileSize: 10 * 1024 * 1024 } }).single('file')
exports.uploadVideo = multer({ storage: videoStorage, limits: { fileSize: 500 * 1024 * 1024 } }).single('file')
exports.uploadModel = multer({ storage: modelStorage, limits: { fileSize: 200 * 1024 * 1024 } }).single('file')

function relativePath(fullPath, subdir) {
  return path.posix.join(subdir, path.basename(fullPath))
}

function formatDate(d) {
  if (!d) return ''
  const date = new Date(d)
  const pad = n => String(n).padStart(2, '0')
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}

function randomPlate() {
  const prefixes = ['京', '沪', '津', '渝', '冀', '豫', '云', '辽', '黑', '湘', '皖', '鲁', '新', '苏', '浙', '赣', '鄂', '桂', '甘', '晋', '蒙', '陕', '吉', '闽', '贵', '粤', '青', '藏', '川', '宁', '琼']
  const letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789'
  const prefix = prefixes[Math.floor(Math.random() * prefixes.length)]
  const letter = letters[Math.floor(Math.random() * letters.length)]
  let num = ''
  for (let i = 0; i < 5; i++) num += chars[Math.floor(Math.random() * chars.length)]
  return prefix + letter + num
}

function randomPlateColor() {
  const colors = ['blue', 'yellow', 'green', 'white', 'black']
  const weights = [60, 20, 12, 5, 3]
  const total = weights.reduce((a, b) => a + b, 0)
  let r = Math.random() * total
  for (let i = 0; i < colors.length; i++) {
    r -= weights[i]
    if (r <= 0) return colors[i]
  }
  return colors[0]
}

function generatePlates(count = 1) {
  return Array.from({ length: count }, () => ({
    plate_no: randomPlate(),
    plate_color: randomPlateColor(),
    plate_type: Math.random() > 0.8 ? 'double' : 'single',
    confidence: 0.85 + Math.random() * 0.14,
    color_conf: 0.8 + Math.random() * 0.19,
    box: [Math.floor(Math.random() * 200), Math.floor(Math.random() * 150), Math.floor(Math.random() * 200) + 100, Math.floor(Math.random() * 150) + 50],
    landmarks: [[10, 10], [100, 10], [100, 40], [10, 40]]
  }))
}

function generateFrames() {
  return Array.from({ length: 8 }, (_, i) => ({
    frame_no: i * 30 + 1,
    timestamp: (i * 1.2).toFixed(1) + 's',
    plate_no: randomPlate(),
    confidence: 0.8 + Math.random() * 0.19
  }))
}

function rowToOutput(row, type = 'image') {
  return {
    id: row.id,
    filename: row.filename,
    path: row.path,
    result_path: row.result_path || '',
    status: row.status,
    size: row.size,
    video_codec: row.video_codec || '',
    transcoded: row.transcoded || 0,
    create_time: formatDate(row.create_time),
    url: '/static/' + row.path,
    result_url: row.result_path ? '/static/' + row.result_path : ''
  }
}

function buildListWhere(req, table) {
  const { keyword = '', status = '', range } = req.query
  let where = 'WHERE 1=1'
  const params = []
  if (status) { where += ' AND status = ?'; params.push(status) }
  if (keyword) { where += ' AND filename LIKE ?'; params.push('%' + keyword + '%') }
  if (range && Array.isArray(range) && range.length === 2) {
    where += ' AND DATE(create_time) BETWEEN ? AND ?'
    params.push(range[0], range[1])
  }
  return { where, params }
}

// ========== 图片 ==========
exports.imageUpload = async (req, res) => {
  if (!req.file) return res.json({ code: 1, message: '缺少文件' })
  const filename = decodeFilename(req.file.originalname)
  const p = relativePath(req.file.path, 'images')
  const result = await query('INSERT INTO plate_images (filename, path, size) VALUES (?, ?, ?)', [filename, p, req.file.size])
  res.json({ code: 0, data: { id: result.insertId, filename, path: p, size: req.file.size, status: 'pending' }, message: '上传成功' })
}

exports.imageList = async (req, res) => {
  const { where, params } = buildListWhere(req, 'plate_images')
  const list = await query(`SELECT * FROM plate_images ${where} ORDER BY id DESC`, params)
  res.json({ code: 0, data: list.map(r => rowToOutput(r, 'image')), message: 'ok' })
}

exports.imageDetect = async (req, res) => {
  const id = Number(req.body.id)
  const [row] = await query('SELECT * FROM plate_images WHERE id = ?', [id])
  if (!row) return res.json({ code: 1, message: '图片不存在' })
  const plates = generatePlates(1 + Math.floor(Math.random() * 2))
  const ext = path.extname(row.path)
  const resultName = path.basename(row.path, ext) + '_result' + ext
  const resultPath = path.posix.join('images', resultName)
  fs.copyFileSync(path.join(UPLOAD_DIR, row.path), path.join(UPLOAD_DIR, resultPath))
  await query('UPDATE plate_images SET status = ?, result_path = ?, plates = ? WHERE id = ?', ['detected', resultPath, JSON.stringify(plates), id])
  await query('INSERT INTO plate_records (filename, type, plates) VALUES (?, ?, ?)', [row.filename, 'image', JSON.stringify(plates)])
  res.json({ code: 0, data: { id, result_path: resultPath, plates }, message: '检测完成' })
}

exports.imageBatchDetect = async (req, res) => {
  const ids = req.body.ids || []
  for (const id of ids) {
    const [row] = await query('SELECT * FROM plate_images WHERE id = ?', [id])
    if (!row || row.status === 'detected') continue
    const plates = generatePlates(1)
    const ext = path.extname(row.path)
    const resultName = path.basename(row.path, ext) + '_result' + ext
    const resultPath = path.posix.join('images', resultName)
    fs.copyFileSync(path.join(UPLOAD_DIR, row.path), path.join(UPLOAD_DIR, resultPath))
    await query('UPDATE plate_images SET status = ?, result_path = ?, plates = ? WHERE id = ?', ['detected', resultPath, JSON.stringify(plates), id])
    await query('INSERT INTO plate_records (filename, type, plates) VALUES (?, ?, ?)', [row.filename, 'image', JSON.stringify(plates)])
  }
  res.json({ code: 0, message: '批量检测完成' })
}

exports.imageDelete = async (req, res) => {
  const id = Number(req.params.id)
  const [row] = await query('SELECT * FROM plate_images WHERE id = ?', [id])
  if (row) {
    try { fs.unlinkSync(path.join(UPLOAD_DIR, row.path)) } catch (e) {}
    if (row.result_path) try { fs.unlinkSync(path.join(UPLOAD_DIR, row.result_path)) } catch (e) {}
  }
  await query('DELETE FROM plate_images WHERE id = ?', [id])
  res.json({ code: 0, message: '删除成功' })
}

exports.imageBatchDelete = async (req, res) => {
  const ids = req.body.ids || []
  for (const id of ids) {
    const [row] = await query('SELECT * FROM plate_images WHERE id = ?', [id])
    if (row) {
      try { fs.unlinkSync(path.join(UPLOAD_DIR, row.path)) } catch (e) {}
      if (row.result_path) try { fs.unlinkSync(path.join(UPLOAD_DIR, row.result_path)) } catch (e) {}
    }
    await query('DELETE FROM plate_images WHERE id = ?', [id])
  }
  res.json({ code: 0, message: '删除成功' })
}

// ========== 视频 ==========
exports.videoUpload = async (req, res) => {
  if (!req.file) return res.json({ code: 1, message: '缺少文件' })
  const filename = decodeFilename(req.file.originalname)
  const p = relativePath(req.file.path, 'videos')
  await query('INSERT INTO plate_videos (filename, path, size, video_codec) VALUES (?, ?, ?, ?)', [filename, p, req.file.size, 'h264'])
  res.json({ code: 0, data: { filename, path: p, size: req.file.size, status: 'pending' }, message: '上传成功' })
}

exports.videoList = async (req, res) => {
  const { where, params } = buildListWhere(req, 'plate_videos')
  const list = await query(`SELECT * FROM plate_videos ${where} ORDER BY id DESC`, params)
  res.json({ code: 0, data: list.map(r => rowToOutput(r, 'video')), message: 'ok' })
}

exports.videoDetect = async (req, res) => {
  const id = Number(req.body.id)
  const [row] = await query('SELECT * FROM plate_videos WHERE id = ?', [id])
  if (!row) return res.json({ code: 1, message: '视频不存在' })
  const frames = generateFrames()
  const ext = path.extname(row.path)
  const resultName = path.basename(row.path, ext) + '_result' + ext
  const resultPath = path.posix.join('videos', resultName)
  fs.copyFileSync(path.join(UPLOAD_DIR, row.path), path.join(UPLOAD_DIR, resultPath))
  await query('UPDATE plate_videos SET status = ?, result_path = ?, frames = ?, video_codec = ?, transcoded = ? WHERE id = ?', ['detected', resultPath, JSON.stringify(frames), 'h264', 1, id])
  await query('INSERT INTO plate_records (filename, type, plates) VALUES (?, ?, ?)', [row.filename, 'video', JSON.stringify(frames.map(f => f.plate_no))])
  res.json({ code: 0, data: { id, result_path: resultPath, frames, video_codec: 'h264', transcoded: 1 }, message: '检测完成' })
}

exports.videoBatchDetect = async (req, res) => {
  const ids = req.body.ids || []
  for (const id of ids) {
    const [row] = await query('SELECT * FROM plate_videos WHERE id = ?', [id])
    if (!row || row.status === 'detected') continue
    const frames = generateFrames()
    const ext = path.extname(row.path)
    const resultName = path.basename(row.path, ext) + '_result' + ext
    const resultPath = path.posix.join('videos', resultName)
    fs.copyFileSync(path.join(UPLOAD_DIR, row.path), path.join(UPLOAD_DIR, resultPath))
    await query('UPDATE plate_videos SET status = ?, result_path = ?, frames = ?, video_codec = ?, transcoded = ? WHERE id = ?', ['detected', resultPath, JSON.stringify(frames), 'h264', 1, id])
  }
  res.json({ code: 0, message: '批量检测完成' })
}

exports.videoDelete = async (req, res) => {
  const id = Number(req.params.id)
  const [row] = await query('SELECT * FROM plate_videos WHERE id = ?', [id])
  if (row) {
    try { fs.unlinkSync(path.join(UPLOAD_DIR, row.path)) } catch (e) {}
    if (row.result_path) try { fs.unlinkSync(path.join(UPLOAD_DIR, row.result_path)) } catch (e) {}
  }
  await query('DELETE FROM plate_videos WHERE id = ?', [id])
  res.json({ code: 0, message: '删除成功' })
}

exports.videoBatchDelete = async (req, res) => {
  const ids = req.body.ids || []
  for (const id of ids) {
    const [row] = await query('SELECT * FROM plate_videos WHERE id = ?', [id])
    if (row) {
      try { fs.unlinkSync(path.join(UPLOAD_DIR, row.path)) } catch (e) {}
      if (row.result_path) try { fs.unlinkSync(path.join(UPLOAD_DIR, row.result_path)) } catch (e) {}
    }
    await query('DELETE FROM plate_videos WHERE id = ?', [id])
  }
  res.json({ code: 0, message: '删除成功' })
}

// ========== 资源 ==========
exports.imageResourceList = exports.imageList
exports.videoResourceList = exports.videoList

exports.downloadImage = async (req, res) => {
  const id = Number(req.params.id)
  const [row] = await query('SELECT * FROM plate_images WHERE id = ?', [id])
  if (!row) return res.status(404).send('Not found')
  const file = path.join(UPLOAD_DIR, row.path)
  if (!fs.existsSync(file)) return res.status(404).send('File not found')
  res.download(file, row.filename)
}

exports.downloadVideo = async (req, res) => {
  const id = Number(req.params.id)
  const [row] = await query('SELECT * FROM plate_videos WHERE id = ?', [id])
  if (!row) return res.status(404).send('Not found')
  const file = path.join(UPLOAD_DIR, row.path)
  if (!fs.existsSync(file)) return res.status(404).send('File not found')
  res.download(file, row.filename)
}

// ========== 日志 ==========
function ensureLogFiles() {
  const today = new Date().toISOString().slice(0, 10)
  const name = `app-${today}.log`
  const p = path.join(LOG_DIR, name)
  if (!fs.existsSync(p)) fs.writeFileSync(p, `[${new Date().toISOString()}] system started\n`)
}
ensureLogFiles()

exports.logList = async (req, res) => {
  ensureLogFiles()
  const { keyword = '' } = req.query
  const files = fs.readdirSync(LOG_DIR)
    .filter(f => f.endsWith('.log') && (!keyword || f.includes(keyword)))
    .map(f => {
      const p = path.join(LOG_DIR, f)
      const stat = fs.statSync(p)
      const date = f.match(/(\d{4}-\d{2}-\d{2})/)?.[1] || ''
      return { name: f, size: stat.size, date }
    })
    .sort((a, b) => b.date.localeCompare(a.date))
  res.json({ code: 0, data: files, message: 'ok' })
}

exports.logPreview = async (req, res) => {
  const { name, lines = 200 } = req.query
  const p = path.join(LOG_DIR, name)
  if (!fs.existsSync(p)) return res.json({ code: 1, message: '文件不存在' })
  const all = fs.readFileSync(p, 'utf8').split('\n')
  const preview = all.slice(-Number(lines)).join('\n')
  res.json({ code: 0, data: preview, message: 'ok' })
}

exports.logDownload = async (req, res) => {
  const p = path.join(LOG_DIR, req.params.name)
  if (!fs.existsSync(p)) return res.status(404).send('Not found')
  res.download(p, req.params.name)
}

exports.logDelete = async (req, res) => {
  const today = new Date().toISOString().slice(0, 10)
  if (req.params.name.includes(today)) return res.status(403).json({ code: 1, message: '当天日志不可删除' })
  const p = path.join(LOG_DIR, req.params.name)
  if (fs.existsSync(p)) fs.unlinkSync(p)
  res.json({ code: 0, message: '删除成功' })
}

// ========== 数据可视化 ==========
exports.dashboardStats = async (req, res) => {
  const [[imgCount], [videoCount], [detectCount], [recordCount]] = await Promise.all([
    query('SELECT COUNT(*) AS total FROM plate_images'),
    query('SELECT COUNT(*) AS total FROM plate_videos'),
    query('SELECT COUNT(*) AS total FROM plate_records'),
    query('SELECT COUNT(*) AS total FROM plate_records')
  ])
  const plateStats = await query('SELECT plate_no, COUNT(*) AS count FROM (SELECT JSON_UNQUOTE(JSON_EXTRACT(plates, "$[*].plate_no")) AS nums FROM plate_images WHERE plates IS NOT NULL) t, JSON_TABLE(t.nums, "$[*]" COLUMNS (plate_no VARCHAR(20) PATH "$")) j GROUP BY plate_no ORDER BY count DESC LIMIT 10')
    .catch(() => [])
  const trend = Array.from({ length: 7 }, (_, i) => {
    const d = new Date(); d.setDate(d.getDate() - 6 + i)
    return { date: d.toISOString().slice(5, 10), value: Math.floor(Math.random() * 40) + 5 }
  })
  res.json({
    code: 0,
    data: {
      imageCount: imgCount.total,
      videoCount: videoCount.total,
      detectCount: detectCount.total,
      recordCount: recordCount.total,
      resultDistribution: [
        { name: '蓝牌', value: 35 },
        { name: '黄牌', value: 22 },
        { name: '绿牌', value: 18 },
        { name: '白牌', value: 12 },
        { name: '其他', value: 8 }
      ],
      trend,
      plateStats: plateStats.length ? plateStats : [
        { plate_no: '京A12345', count: 12 },
        { plate_no: '沪B67890', count: 8 },
        { plate_no: '粤C54321', count: 6 }
      ]
    },
    message: 'ok'
  })
}

exports.recentRecords = async (req, res) => {
  const limit = Number(req.query.limit) || 10
  const rows = await query('SELECT * FROM plate_records ORDER BY id DESC LIMIT ?', [limit])
  res.json({ code: 0, data: rows.map(r => ({ id: r.id, filename: r.filename, type: r.type, create_time: formatDate(r.create_time) })), message: 'ok' })
}

// ========== 系统监控 ==========
exports.systemMonitor = async (req, res) => {
  const totalMem = os.totalmem()
  const freeMem = os.freemem()
  const cpus = os.cpus()
  res.json({
    code: 0,
    data: {
      cpu_percent: (Math.random() * 0.3 + 0.1).toFixed(4),
      cpu_cores: cpus.length,
      memory_percent: ((totalMem - freeMem) / totalMem).toFixed(4),
      memory_used: totalMem - freeMem,
      memory_total: totalMem,
      disk_percent: 0.45,
      net_sent: 1024 * 1024 * 123,
      net_recv: 1024 * 1024 * 456,
      os: os.type() + ' ' + os.release(),
      uptime: os.uptime()
    },
    message: 'ok'
  })
}

// ========== 模型管理 ==========
exports.modelList = async (req, res) => {
  const list = await query('SELECT * FROM plate_models ORDER BY id DESC')
  res.json({ code: 0, data: list, message: 'ok' })
}

exports.modelUpload = async (req, res) => {
  if (!req.file) return res.json({ code: 1, message: '缺少文件' })
  const filename = decodeFilename(req.file.originalname)
  const result = await query('INSERT INTO plate_models (filename, name, version, accuracy) VALUES (?, ?, ?, ?)', [filename, filename.replace(/\.[^.]+$/, ''), '1.0', 0.95])
  res.json({ code: 0, data: { id: result.insertId }, message: '上传成功' })
}

exports.modelUpdate = async (req, res) => {
  const id = Number(req.params.id)
  const fields = ['name', 'dataset', 'base_model', 'version', 'accuracy', 'description', 'is_default', 'is_loaded']
  const data = {}
  fields.forEach(f => { if (req.body[f] !== undefined) data[f] = req.body[f] })
  const cols = Object.keys(data)
  if (!cols.length) return res.json({ code: 0, message: '无更新' })
  await query(`UPDATE plate_models SET ${cols.map(c => `${c} = ?`).join(',')} WHERE id = ?`, [...Object.values(data), id])
  res.json({ code: 0, message: '更新成功' })
}

exports.modelLoad = async (req, res) => {
  const id = Number(req.params.id)
  await query('UPDATE plate_models SET is_loaded = 0')
  await query('UPDATE plate_models SET is_loaded = 1 WHERE id = ?', [id])
  res.json({ code: 0, message: '加载成功' })
}

exports.modelDelete = async (req, res) => {
  const id = Number(req.params.id)
  const [row] = await query('SELECT * FROM plate_models WHERE id = ?', [id])
  if (row && row.filename) {
    const p = path.join(MODEL_DIR, row.filename)
    if (fs.existsSync(p)) fs.unlinkSync(p)
  }
  await query('DELETE FROM plate_models WHERE id = ?', [id])
  res.json({ code: 0, message: '删除成功' })
}

// ========== LLM / 多模态 ==========
exports.textModels = async (req, res) => {
  res.json({ code: 0, data: [{ id: 'qwen-turbo', name: '通义千问 Turbo' }, { id: 'gpt-3.5', name: 'GPT-3.5' }], message: 'ok' })
}

exports.visionModels = async (req, res) => {
  res.json({ code: 0, data: [{ id: 'qwen-vl', name: '通义千问 VL' }, { id: 'gpt-4v', name: 'GPT-4 Vision' }], message: 'ok' })
}

exports.chatText = async (req, res) => {
  const { message } = req.body
  const reply = `收到你的问题：“${message || ''}”。当前为演示模式，后续可接入真实大模型 API。`
  res.json({ code: 0, data: { reply }, message: 'ok' })
}

exports.chatTextStream = async (req, res) => {
  const { message } = req.body
  const reply = `收到你的问题：“${message || ''}”。当前为演示模式，后续可接入真实大模型 API。`
  res.setHeader('Content-Type', 'text/plain; charset=utf-8')
  res.setHeader('Cache-Control', 'no-cache')
  const chunks = reply.split('')
  let i = 0
  const timer = setInterval(() => {
    if (i >= chunks.length) { clearInterval(timer); return res.end() }
    res.write(chunks[i])
    i++
  }, 50)
}

exports.chatVision = exports.chatText
exports.chatVisionStream = exports.chatTextStream

// ========== 文档 ==========
exports.projectDocs = async (req, res) => {
  res.json({
    code: 0,
    data: {
      system_name: '车牌检测识别平台',
      base_url: 'http://127.0.0.1:9999',
      abilities: '图片检测、视频检测、资源管理、系统监控、模型管理、LLM、多模态问答'
    },
    message: 'ok'
  })
}
