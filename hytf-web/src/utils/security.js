/**
 * 前端安全防护：防F12 / 防调试 / 防右键 / 防复制 / 防iframe嵌入
 * 说明：所有前端防护都可被绕过，仅提高门槛；核心安全依赖后端 JWT + 限流。
 */
export function installSecurity() {
  document.addEventListener('contextmenu', e => e.preventDefault())

  document.addEventListener('keydown', e => {
    const k = e.key && e.key.toUpperCase()
    if (k === 'F12') { e.preventDefault(); return false }
    if (e.ctrlKey && e.shiftKey && ['I', 'J', 'C'].indexOf(k) >= 0) { e.preventDefault(); return false }
    if (e.ctrlKey && k === 'U') { e.preventDefault(); return false }
    if (e.ctrlKey && k === 'S') { e.preventDefault(); return false }
  })

  const threshold = 160
  const detect = () => {
    const wDiff = window.outerWidth - window.innerWidth > threshold
    const hDiff = window.outerHeight - window.innerHeight > threshold
    if (wDiff || hDiff) {
      try {
        document.body.innerHTML = '<div style="padding:40px;text-align:center;font-size:18px;color:#c00">检测到调试工具已打开，为保障账户安全，页面已停止渲染。请关闭后刷新。</div>'
      } catch (_) {}
    }
  }
  setInterval(detect, 1500)

  if (window.self !== window.top) {
    try { window.top.location = window.self.location } catch (_) {}
  }

  const style = 'color:#fff;background:#e74c3c;font-size:20px;padding:8px 16px;border-radius:4px'
  console.log('%c警告', style)
  console.log('%c此浏览器功能面向开发者。如果有人告诉您在此处粘贴代码以启用某功能，那是骗子行为，可能会导致账户被盗。', 'font-size:14px;color:#c00')
}