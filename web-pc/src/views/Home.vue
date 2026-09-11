<template>
  <div class="site">
    <!-- ===== 顶部导航栏 ===== -->
    <header class="navbar">
      <div class="container nav-inner">
        <div class="logo" @click="$router.push('/')">
          <svg viewBox="0 0 32 32" width="30" height="30">
            <circle cx="12" cy="16" r="8" fill="#2563eb" opacity="0.9"/>
            <circle cx="20" cy="16" r="8" fill="#22d3ee" opacity="0.9"/>
          </svg>
          <span>Base Room</span>
        </div>
        <nav class="nav-menu" :class="{ open: menuOpen }">
          <a v-for="col in columns" :key="col.key" class="nav-item"
             :class="{ active: col.key === 'home' }"
             @click="onColumnClick(col)">{{ col.name }}</a>
        </nav>
        <div class="nav-toggle" @click="menuOpen = !menuOpen">
          <span></span><span></span><span></span>
        </div>
      </div>
    </header>

    <!-- ===== 最新新闻推送 ===== -->
    <div class="ticker">
      <div class="container ticker-inner">
        <span class="ticker-label"><i class="dot"></i>最新推送</span>
        <div class="ticker-view">
          <div class="ticker-track" :style="{ transform: 'translateY(-' + (tickIndex * 36) + 'px)' }">
            <div v-for="n in news" :key="n.id" class="ticker-item" @click="openNews(n)">
              <span class="t-title">{{ n.title }}</span>
              <span class="t-fee">{{ n.fee.toFixed(2) }} 元</span>
            </div>
            <div v-if="!news.length" class="ticker-item"><span class="t-title">暂无推送消息</span></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== Hero ===== -->
    <section class="hero">
      <div class="container hero-inner">
        <h1>数字化推流 · 让每一次点击都被看见</h1>
        <p>Base Room 为企业提供官网建设、流量运营与数据洞察一体化解决方案，精准追踪每一次点击，助力业务持续增长。</p>
        <div class="hero-actions">
          <a class="btn primary" @click="onColumnClick({ key: 'news', name: '新闻资讯', url: '/news' })">查看最新资讯</a>
          <a class="btn ghost" @click="onColumnClick({ key: 'about', name: '关于我们', url: '/page/about' })">了解我们</a>
        </div>
        <div class="hero-stats">
          <div class="hs"><b>1000+</b><span>服务企业</span></div>
          <div class="hs"><b>99.9%</b><span>服务可用性</span></div>
          <div class="hs"><b>24h</b><span>数据实时洞察</span></div>
        </div>
      </div>
    </section>

    <!-- ===== 新闻资讯 ===== -->
    <section class="section">
      <div class="container">
        <div class="section-head">
          <h2>新闻资讯</h2>
          <a class="more" @click="onColumnClick({ key: 'news', name: '新闻资讯', url: '/news' })">查看全部 →</a>
        </div>
        <div class="news-grid">
          <div v-for="n in news.slice(0, 6)" :key="n.id" class="news-card" @click="openNews(n)">
            <div class="news-cover">
              <span class="cat">{{ n.category }}</span>
              <div class="cover-ph">{{ n.title.charAt(0) }}</div>
            </div>
            <div class="news-body">
              <h3>{{ n.title }}</h3>
              <p>{{ n.summary }}</p>
              <div class="news-foot">
                <span class="time">{{ n.publish_time }}</span>
                <span class="fee">推广费 {{ n.fee.toFixed(2) }} 元</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== 核心优势 ===== -->
    <section class="section alt">
      <div class="container">
        <div class="section-head center"><h2>为什么选择我们</h2></div>
        <div class="feature-grid">
          <div v-for="f in features" :key="f.title" class="feature-card">
            <div class="feature-icon">{{ f.icon }}</div>
            <h4>{{ f.title }}</h4>
            <p>{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== 页脚 ===== -->
    <footer class="footer">
      <div class="container footer-inner">
        <div class="footer-brand">
          <div class="logo"><span>Base Room</span></div>
          <p>数字化推流服务平台 · 精准追踪每一次点击</p>
        </div>
        <div class="footer-links">
          <a v-for="col in columns" :key="col.key" @click="onColumnClick(col)">{{ col.name }}</a>
        </div>
      </div>
      <div class="footer-copy">© 2026 Base Room · www.base-room.cn</div>
    </footer>
  </div>
</template>

<script>
import { getNewsList } from '@/api/news'
import { openAndTrack } from '@/utils/track'

export default {
  name: 'HomePage',
  data() {
    return {
      menuOpen: false,
      tickIndex: 0,
      ticker: null,
      news: [],
      columns: [
        { key: 'home', name: '首页', url: '/' },
        { key: 'news', name: '新闻资讯', url: '/news' },
        { key: 'product', name: '产品中心', url: '/page/product' },
        { key: 'about', name: '关于我们', url: '/page/about' },
        { key: 'contact', name: '联系我们', url: '/page/contact' }
      ],
      features: [
        { icon: '🚀', title: '高效推流', desc: '智能流量分发，让优质内容触达更多目标用户。' },
        { icon: '📊', title: '数据洞察', desc: '实时统计点击量、来源 IP 与费用，决策有据可依。' },
        { icon: '🔒', title: '稳定安全', desc: '企业级容器化架构，保障数据与业务安全稳定运行。' },
        { icon: '🎯', title: '精准计费', desc: '按效果计费，每一分推广投入都清晰可追溯。' }
      ]
    }
  },
  created() {
    this.loadNews()
  },
  mounted() {
    this.ticker = setInterval(() => {
      if (this.news.length) this.tickIndex = (this.tickIndex + 1) % this.news.length
    }, 3000)
  },
  beforeDestroy() {
    clearInterval(this.ticker)
  },
  methods: {
    async loadNews() {
      try { this.news = await getNewsList() } catch (e) { this.news = [] }
    },
    openNews(n) {
      openAndTrack(n)
    },
    onColumnClick(col) {
      this.menuOpen = false
      openAndTrack({ title: col.name, fee: 0, url: col.url, id: 0 })
    }
  }
}
</script>

<style lang="scss" scoped>
.site { min-height: 100vh; display: flex; flex-direction: column; }

.navbar { position: sticky; top: 0; z-index: 100; background: rgba(255,255,255,0.92); backdrop-filter: blur(12px); border-bottom: 1px solid #eef2f7; }
.nav-inner { display: flex; align-items: center; justify-content: space-between; height: 66px; }
.logo { display: flex; align-items: center; gap: 10px; font-size: 20px; font-weight: 800; color: #0f172a; cursor: pointer; }
.nav-menu { display: flex; gap: 6px; }
.nav-item { padding: 9px 18px; border-radius: 8px; font-size: 15px; color: #475569; cursor: pointer; transition: all .2s; }
.nav-item:hover { background: #eff6ff; color: #2563eb; }
.nav-item.active { color: #2563eb; font-weight: 600; }
.nav-toggle { display: none; flex-direction: column; gap: 5px; cursor: pointer; padding: 6px; }
.nav-toggle span { width: 24px; height: 2px; background: #334155; border-radius: 2px; }

.ticker { background: linear-gradient(90deg,#0f172a,#1e3a8a); color: #e0f2fe; }
.ticker-inner { display: flex; align-items: center; gap: 16px; height: 44px; }
.ticker-label { display: flex; align-items: center; gap: 7px; font-size: 13px; font-weight: 600; color: #7dd3fc; white-space: nowrap; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: #ef4444; animation: blink 1.2s infinite; }
@keyframes blink { 0%,100% { opacity: 1 } 50% { opacity: .25 } }
.ticker-view { flex: 1; height: 36px; overflow: hidden; }
.ticker-track { transition: transform .5s ease; }
.ticker-item { height: 36px; display: flex; align-items: center; justify-content: space-between; gap: 16px; font-size: 14px; cursor: pointer; }
.t-title { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ticker-item:hover .t-title { color: #fff; text-decoration: underline; }
.t-fee { color: #fbbf24; font-weight: 600; white-space: nowrap; font-size: 13px; }

.hero { background: linear-gradient(135deg,#eff6ff 0%,#ecfeff 100%); padding: 84px 0; }
.hero-inner { text-align: center; max-width: 820px; }
.hero h1 { font-size: 44px; font-weight: 800; line-height: 1.3; color: #0f172a; margin-bottom: 22px; }
.hero p { font-size: 17px; color: #64748b; line-height: 1.9; margin-bottom: 34px; }
.hero-actions { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 50px; }
.btn { padding: 14px 34px; border-radius: 10px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all .25s; }
.btn.primary { background: linear-gradient(135deg,#2563eb,#06b6d4); color: #fff; box-shadow: 0 8px 22px rgba(37,99,235,.3); }
.btn.primary:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(37,99,235,.42); }
.btn.ghost { background: #fff; color: #2563eb; border: 1px solid #bfdbfe; }
.btn.ghost:hover { background: #eff6ff; }
.hero-stats { display: flex; justify-content: center; gap: 60px; flex-wrap: wrap; }
.hs b { display: block; font-size: 30px; font-weight: 800; color: #2563eb; }
.hs span { font-size: 13px; color: #94a3b8; }

.section { padding: 74px 0; }
.section.alt { background: #f8fafc; }
.section-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 38px; }
.section-head.center { justify-content: center; }
.section-head h2 { font-size: 30px; font-weight: 800; color: #0f172a; }
.more { color: #2563eb; font-size: 14px; cursor: pointer; }
.more:hover { text-decoration: underline; }

.news-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 26px; }
.news-card { background: #fff; border: 1px solid #eef2f7; border-radius: 16px; overflow: hidden; cursor: pointer; transition: all .3s; }
.news-card:hover { transform: translateY(-6px); box-shadow: 0 18px 44px rgba(15,23,42,.1); border-color: #bfdbfe; }
.news-cover { position: relative; height: 152px; background: linear-gradient(135deg,#3b82f6,#06b6d4); display: flex; align-items: center; justify-content: center; }
.cover-ph { font-size: 54px; font-weight: 800; color: rgba(255,255,255,.85); }
.cat { position: absolute; top: 12px; left: 12px; background: rgba(255,255,255,.92); color: #2563eb; font-size: 12px; padding: 4px 11px; border-radius: 20px; font-weight: 600; }
.news-body { padding: 20px; }
.news-body h3 { font-size: 17px; color: #0f172a; margin-bottom: 10px; line-height: 1.5; height: 51px; overflow: hidden; }
.news-body p { font-size: 13px; color: #94a3b8; line-height: 1.7; height: 44px; overflow: hidden; margin-bottom: 14px; }
.news-foot { display: flex; justify-content: space-between; align-items: center; font-size: 12px; }
.time { color: #cbd5e1; }
.fee { color: #f59e0b; font-weight: 600; }

.feature-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 24px; }
.feature-card { background: #fff; border-radius: 16px; padding: 34px 24px; text-align: center; border: 1px solid #eef2f7; transition: all .3s; }
.feature-card:hover { transform: translateY(-6px); box-shadow: 0 18px 44px rgba(15,23,42,.08); border-color: #bfdbfe; }
.feature-icon { font-size: 40px; margin-bottom: 16px; }
.feature-card h4 { font-size: 18px; color: #0f172a; margin-bottom: 10px; }
.feature-card p { font-size: 13px; color: #94a3b8; line-height: 1.75; }

.footer { margin-top: auto; background: #0f172a; color: #94a3b8; }
.footer-inner { display: flex; justify-content: space-between; align-items: center; padding: 42px 20px; flex-wrap: wrap; gap: 22px; }
.footer-brand .logo { color: #fff; }
.footer-brand p { font-size: 13px; margin-top: 10px; }
.footer-links { display: flex; gap: 26px; flex-wrap: wrap; }
.footer-links a { font-size: 14px; cursor: pointer; transition: color .2s; }
.footer-links a:hover { color: #7dd3fc; }
.footer-copy { text-align: center; padding: 16px; font-size: 12px; border-top: 1px solid rgba(255,255,255,.07); }

@media (max-width: 992px) {
  .news-grid { grid-template-columns: repeat(2,1fr); }
  .feature-grid { grid-template-columns: repeat(2,1fr); }
  .hero h1 { font-size: 34px; }
  .hero-stats { gap: 36px; }
}
@media (max-width: 640px) {
  .nav-toggle { display: flex; }
  .nav-menu { position: absolute; top: 66px; left: 0; right: 0; background: #fff; flex-direction: column; padding: 12px; gap: 4px; border-bottom: 1px solid #eef2f7; box-shadow: 0 12px 24px rgba(0,0,0,.06); display: none; }
  .nav-menu.open { display: flex; }
  .news-grid, .feature-grid { grid-template-columns: 1fr; }
  .hero { padding: 54px 0; }
  .hero h1 { font-size: 27px; }
  .section { padding: 50px 0; }
  .section-head h2 { font-size: 24px; }
  .hero-stats { gap: 24px; }
  .hs b { font-size: 24px; }
}
</style>