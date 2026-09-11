<template>
  <div class="page">
    <header class="navbar">
      <div class="container nav-inner">
        <div class="logo" @click="$router.push('/')">
          <svg viewBox="0 0 32 32" width="30" height="30">
            <circle cx="12" cy="16" r="8" fill="#2563eb" opacity="0.9"/>
            <circle cx="20" cy="16" r="8" fill="#22d3ee" opacity="0.9"/>
          </svg>
          <span>Base Room</span>
        </div>
        <a class="back" @click="$router.push('/')">返回首页</a>
      </div>
    </header>

    <div class="container list-wrap">
      <h1 class="page-title">新闻资讯</h1>
      <p class="page-desc">共 {{ news.length }} 条资讯，点击任意标题将在新窗口打开并记录访问数据</p>
      <div class="list">
        <div v-for="n in news" :key="n.id" class="row" @click="openNews(n)">
          <div class="row-main">
            <span class="cat">{{ n.category }}</span>
            <h3>{{ n.title }}</h3>
            <p>{{ n.summary }}</p>
          </div>
          <div class="row-side">
            <span class="fee">{{ n.fee.toFixed(2) }} 元</span>
            <span class="time">{{ n.publish_time }}</span>
            <span class="go">查看详情 →</span>
          </div>
        </div>
        <div v-if="!news.length" class="empty">暂无新闻资讯</div>
      </div>
    </div>
  </div>
</template>

<script>
import { getNewsList } from '@/api/news'
import { openAndTrack } from '@/utils/track'

export default {
  name: 'NewsListPage',
  data() { return { news: [] } },
  created() { this.load() },
  methods: {
    async load() {
      try { this.news = await getNewsList() } catch (e) { this.news = [] }
    },
    openNews(n) { openAndTrack(n) }
  }
}
</script>

<style lang="scss" scoped>
.navbar { background: #fff; border-bottom: 1px solid #eef2f7; position: sticky; top: 0; z-index: 100; }
.nav-inner { display: flex; align-items: center; justify-content: space-between; height: 66px; }
.logo { display: flex; align-items: center; gap: 10px; font-size: 20px; font-weight: 800; color: #0f172a; cursor: pointer; }
.back { color: #2563eb; font-size: 14px; cursor: pointer; }
.list-wrap { padding: 44px 20px 70px; }
.page-title { font-size: 30px; font-weight: 800; margin-bottom: 10px; }
.page-desc { font-size: 14px; color: #94a3b8; margin-bottom: 30px; }
.row { display: flex; justify-content: space-between; gap: 24px; padding: 24px; background: #fff; border: 1px solid #eef2f7; border-radius: 14px; margin-bottom: 16px; cursor: pointer; transition: all .25s; }
.row:hover { border-color: #bfdbfe; box-shadow: 0 12px 32px rgba(15,23,42,.07); transform: translateY(-2px); }
.cat { display: inline-block; background: #eff6ff; color: #2563eb; font-size: 12px; padding: 3px 11px; border-radius: 20px; margin-bottom: 10px; font-weight: 600; }
.row-main { flex: 1; min-width: 0; }
.row-main h3 { font-size: 18px; color: #0f172a; margin-bottom: 8px; line-height: 1.5; }
.row-main p { font-size: 13px; color: #94a3b8; line-height: 1.75; }
.row-side { text-align: right; white-space: nowrap; flex-shrink: 0; }
.fee { display: block; color: #f59e0b; font-weight: 700; font-size: 17px; margin-bottom: 8px; }
.time { display: block; font-size: 12px; color: #cbd5e1; margin-bottom: 10px; }
.go { font-size: 13px; color: #2563eb; }
.empty { text-align: center; color: #94a3b8; padding: 70px; background: #f8fafc; border-radius: 14px; }
@media (max-width: 640px) {
  .row { flex-direction: column; gap: 14px; }
  .row-side { text-align: left; }
  .fee, .time { display: inline-block; margin-right: 16px; }
}
</style>