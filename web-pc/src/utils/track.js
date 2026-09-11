import { recordClick } from '@/api/news'

/**
 * 统一的链接点击处理：埋点记录 + 新窗口打开
 * 点击时间与真实 IP 由后端自动记录，前端只需上报 标题 / 费用 / 链接
 * @param {Object} item 需包含 title、fee、url，可选 id
 */
export function openAndTrack(item) {
  if (!item) return

  const payload = {
    news_id: item.id || item.news_id || 0,
    title: item.title || '',
    fee: item.fee || 0,
    url: item.url || ''
  }

  // 上报点击（失败不阻塞跳转，保证用户体验）
  recordClick(payload).catch(() => {})

  // 打开新窗口
  if (payload.url) {
    window.open(payload.url, '_blank', 'noopener,noreferrer')
  }
}