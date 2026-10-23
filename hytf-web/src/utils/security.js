/**
 * 前端安全防护：防F12 / 防调试 / 防iframe嵌入
 * 说明：已移除"窗口尺寸差"启发式检测——书签栏/侧边栏/竖排标签/缩放等
 *       正常浏览器界面均会造成误报并遮挡真实用户；核心安全依赖后端 JWT + 限流。
 */
export function installSecurity() {

  document.addEventListener('keydown', e => {
    const k = e.key && e.key.toUpperCase()
    if (k === 'F12') { e.preventDefault(); return false }
    if (e.ctrlKey && e.shiftKey && ['I', 'J', 'C'].indexOf(k) >= 0) { e.preventDefault(); return false }
    if (e.ctrlKey && k === 'U') { e.preventDefault(); return false }
    if (e.ctrlKey && k === 'S') { e.preventDefault(); return false }
  })

  if (window.self !== window.top) {
    try { window.top.location = window.self.location } catch (_) {}
  }

  const style = 'color:#fff;background:#e74c3c;font-size:20px;padding:8px 16px;border-radius:4px'
  console.log('%c警告', style)
  console.log('%c此浏览器功能面向开发者。如果有人告诉您在此处粘贴代码以启用某功能，那是骗子行为，可能会导致账户被盗。', 'font-size:16px;color:#c00')
}