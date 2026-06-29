const IMAGE_CACHE_KEY = 'plate_image_detection_cache'
const VIDEO_CACHE_KEY = 'plate_video_detection_cache'
const MULTIMODAL_CONTEXT_KEY = 'plate_multimodal_context'

export const getImageCache = () => {
  try { return JSON.parse(localStorage.getItem(IMAGE_CACHE_KEY) || '{}') } catch (e) { return {} }
}
export const setImageCache = data => localStorage.setItem(IMAGE_CACHE_KEY, JSON.stringify(data))
export const clearImageCache = () => localStorage.removeItem(IMAGE_CACHE_KEY)

export const getVideoCache = () => {
  try { return JSON.parse(localStorage.getItem(VIDEO_CACHE_KEY) || '{}') } catch (e) { return {} }
}
export const setVideoCache = data => localStorage.setItem(VIDEO_CACHE_KEY, JSON.stringify(data))
export const clearVideoCache = () => localStorage.removeItem(VIDEO_CACHE_KEY)

export const getMultimodalContext = () => {
  try { return JSON.parse(localStorage.getItem(MULTIMODAL_CONTEXT_KEY) || '[]') } catch (e) { return [] }
}
export const setMultimodalContext = data => localStorage.setItem(MULTIMODAL_CONTEXT_KEY, JSON.stringify(data))

export const formatSize = bytes => {
  if (bytes === undefined || bytes === null) return '-'
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  let i = 0
  let size = Number(bytes)
  while (size >= 1024 && i < units.length - 1) { size /= 1024; i++ }
  return size.toFixed(i === 0 ? 0 : 2) + ' ' + units[i]
}

export const formatPercent = (value, digits = 1) => {
  if (value === undefined || value === null) return '-'
  return (Number(value) * 100).toFixed(digits) + '%'
}

export const formatDate = (date, fmt = 'YYYY-MM-DD HH:mm:ss') => {
  if (!date) return '-'
  const d = new Date(date)
  const pad = n => String(n).padStart(2, '0')
  const map = {
    'YYYY': d.getFullYear(),
    'MM': pad(d.getMonth() + 1),
    'DD': pad(d.getDate()),
    'HH': pad(d.getHours()),
    'mm': pad(d.getMinutes()),
    'ss': pad(d.getSeconds())
  }
  return fmt.replace(/YYYY|MM|DD|HH|mm|ss/g, m => map[m])
}

export const plateTypeLabel = type => {
  const map = {
    'single': '单层',
    'double': '双层',
    'new_energy': '新能源',
    'unknown': '未知'
  }
  return map[type] || type || '未知'
}

export const plateColorLabel = color => {
  const map = {
    'blue': '蓝牌',
    'yellow': '黄牌',
    'green': '绿牌',
    'white': '白牌',
    'black': '黑牌',
    'gradient_green': '渐变绿'
  }
  return map[color] || color || '未知'
}

export const detectionSummary = result => {
  if (!result || !result.plates || !result.plates.length) return '未识别到车牌'
  const items = result.plates.map(p => `${p.plate_no}(${plateColorLabel(p.plate_color)})`)
  return '识别到 ' + result.plates.length + ' 个车牌：' + items.join('、')
}

export const matchDetectedName = (original, detectedList) => {
  if (!original || !detectedList) return null
  const name = original.name || original.filename || ''
  const base = name.replace(/\.[^.]+$/, '')
  return detectedList.find(d => {
    const dn = d.name || d.filename || ''
    return dn === base + '_result' + (dn.match(/\.[^.]+$/) || [''])[0] || dn.startsWith(base)
  })
}

export const buildLinePath = (points, width, height, min, max) => {
  if (!points || points.length < 2) return ''
  const range = max - min || 1
  const stepX = width / (points.length - 1)
  return points.map((v, i) => {
    const x = i * stepX
    const y = height - ((v - min) / range) * height
    return (i === 0 ? 'M' : 'L') + x + ',' + y
  }).join(' ')
}

export const handleReq = async (promise, options = {}) => {
  try {
    const res = await promise
    return options.raw ? res : (res?.data ?? res)
  } catch (e) {
    const msg = e?.response?.data?.message || e.message || '请求失败'
    if (options.silent) throw e
    if (typeof window !== 'undefined' && window.Vue && window.Vue.prototype && window.Vue.prototype.$message) {
      window.Vue.prototype.$message.error(msg)
    }
    throw e
  }
}

export const staticImageUrl = path => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  const base = process.env.VUE_APP_BASE_API || ''
  // 后端 path 为 images/<filename>，直接拼 /static/ 即可
  return base + '/static/' + path.replace(/^\//, '')
}

export const staticVideoUrl = path => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  const base = process.env.VUE_APP_BASE_API || ''
  // 后端 path 为 videos/<filename>，直接拼 /static/ 即可
  return base + '/static/' + path.replace(/^\//, '')
}

export const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  window.URL.revokeObjectURL(url)
}
