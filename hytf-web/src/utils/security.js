/**
 * 鍓嶇瀹夊叏闃叉姢锛氶槻F12 / 闃茶皟璇?/ 闃插彸閿?/ 闃插鍒?/ 闃瞚frame宓屽叆
 * 璇存槑锛氭墍鏈夊墠绔槻鎶ら兘鍙缁曡繃锛屼粎鎻愰珮闂ㄦ锛涙牳蹇冨畨鍏ㄤ緷璧栧悗绔?JWT + 闄愭祦銆?
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
        document.body.innerHTML = '<div style="padding:40px;text-align:center;font-size:18px;color:#c00">妫€娴嬪埌璋冭瘯宸ュ叿宸叉墦寮€锛屼负淇濋殰璐︽埛瀹夊叏锛岄〉闈㈠凡鍋滄娓叉煋銆傝鍏抽棴鍚庡埛鏂般€?/div>'
      } catch (_) {}
    }
  }
  setInterval(detect, 1500)

  if (window.self !== window.top) {
    try { window.top.location = window.self.location } catch (_) {}
  }

  const style = 'color:#fff;background:#e74c3c;font-size:20px;padding:8px 16px;border-radius:4px'
  console.log('%c璀﹀憡', style)
  console.log('%c姝ゆ祻瑙堝櫒鍔熻兘闈㈠悜寮€鍙戣€呫€傚鏋滄湁浜哄憡璇夋偍鍦ㄦ澶勭矘璐翠唬鐮佷互鍚敤鏌愬姛鑳斤紝閭ｆ槸楠楀瓙琛屼负锛屽彲鑳戒細瀵艰嚧璐︽埛琚洍銆?, 'font-size:14px;color:#c00')
}