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
        <a class="back" @click="$router.push('/news')">返回新闻列表</a>
      </div>
    </header>

    <div class="container detail" v-if="news">
      <span class="cat">{{ news.category }}</span>
      <h1>{{ news.title }}</h1>
      <div class="meta">
        <span>{{ news.publish_time }}</span>
        <span class="fee">推广费 {{ Number(news.fee).toFixed(2) }} 元</span>
      </div>
      <div class="content">
        <p>{{ news.summary }}</p>
        <p>本条资讯由 Base Room 推流平台分发，系统已自动记录本次访问的标题、点击时间、IP 地址与费用信息，可在管理后台「交易信息」栏目中查看完整统计。</p>
      </div>
      <a class="btn" v-if="news.url" @click="openNews(news)">前往原文链接 →</a>
    </div>

    <div class="container detail" v-else>
      <p class="empty">新闻不存在或已下架</p>
    </div>
  </div>
</template>

<script>
import { getNewsDetail } from '@/api/news'
import { openAndTrack } from '@/utils/track'

export default {
  name: 'NewsDetailPage',
  data() { return { news: null } },
  created() { this.load() },
  methods: {
    async load() {
      try { this.news = await getNewsDetail(this.$route.params.id) } catch (e) { this.news = null }
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
.detail { padding: 50px 20px 80px; max-width: 840px; }
.cat { display: inline-block; background: #eff6ff; color: #2563eb; font-size: 12px; padding: 4px 13px; border-radius: 20px; margin-bottom: 18px; font-weight: 600; }
.detail h1 { font-size: 31px; color: #0f172a; line-height: 1.45; margin-bottom: 18px; font-weight: 800; }
.meta { display: flex; gap: 24px; font-size: 13px; color: #94a3b8; margin-bottom: 30px; padding-bottom: 22px; border-bottom: 1px solid #eef2f7; flex-wrap: wrap; }
.fee { color: #f59e0b; font-weight: 600; }
.content p { font-size: 16px; color: #475569; line-height: 2.1; margin-bottom: 18px; }
.btn { display: inline-block; margin-top: 16px; padding: 13px 30px; background: linear-gradient(135deg,#2563eb,#06b6d4); color: #fff; border-radius: 10px; font-weight: 600; cursor: pointer; transition: all .25s; }
.btn:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(37,99,235,.35); }
.empty { text-align: center; color: #94a3b8; padding: 80px 0; }
@media (max-width: 640px) {
  .detail h1 { font-size: 24px; }
  .content p { font-size: 15px; }
}
</style>