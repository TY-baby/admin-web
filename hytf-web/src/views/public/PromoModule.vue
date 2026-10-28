<!-- 新文件：D:\work\project\hywork\project\hytf\hytf-web\src\views\public\PromoModule.vue -->
<template>
  <div class="detail" :class="isRecruit ? 'theme-recruit' : 'theme-union'">
    <header class="d-hero">
      <div class="d-badge"><i class="el-icon-medal"></i> 官方认证 · {{ isRecruit ? '招聘宣传' : '直播工会宣传' }}</div>
      <h1 v-if="section">{{ fmt(shortTitle) }}</h1>
    </header>
    <main class="d-container">
      <article class="d-block" v-if="section">
        <h2 class="d-title">{{ fmt(section.title) }}</h2>
        <p class="d-para" v-for="(p, j) in section.paras" :key="j">{{ fmt(p) }}</p>
      </article>
      <div class="d-actions">
        <a class="d-btn d-btn-ghost" :href="'#/book/' + code"><i class="el-icon-back"></i> 返回推广页</a>
        <a class="d-btn d-btn-primary" :href="'#/book/' + code + '/detail'"><i class="el-icon-document"></i> 查看全文</a>
      </div>
    </main>
    <footer class="d-footer">
      <div class="d-foot-brand">{{ company }} · HYTF</div>
      <p>版权声明：转载此文是出于传递更多信息之目的。广告内容请自行辨别，本站不参与任何推荐与导购。</p>
    </footer>
  </div>
</template>

<script>
import { UNION_FULL, RECRUIT_FULL } from './promoContent'

export default {
  name: 'PromoModule',
  data() { return { promoContent: '', company: '' } },
  computed: {
    code() { return this.$route.params.code },
    idx() { return Number(this.$route.params.idx || 0) },
    isRecruit() { return this.promoContent === '招聘宣传' },
    sections() { return this.isRecruit ? RECRUIT_FULL : UNION_FULL },
    section() { return this.sections[this.idx] || null },
    shortTitle() {
      if (!this.section) return ''
      const t = this.section.title
      return t.indexOf('｜') > -1 ? t.split('｜')[0].replace(/^[一二三四]、/, '') : t.replace(/^[一二三四]、/, '')
    }
  },
  mounted() { this.loadInfo() },
  methods: {
    fmt(t) { return String(t || '').replace(/\{company\}/g, this.company) },
    loadInfo() {
      const base = (process.env.VUE_APP_API_BASE || '') + '/api/v1/public/novel_promo/'
      fetch(base + encodeURIComponent(this.code))
          .then(r => r.json())
          .then(d => {
            if (d && d.code === 0 && d.data) {
              this.promoContent = d.data.promo_content || ''
              this.company = d.data.company_name || ''
              if (this.company) document.title = this.company
            }
          })
          .catch(() => {})
    }
  }
}
</script>

<style scoped lang="scss">
.detail { font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif; color: #2c2c3a; background: #fff;
  --c1: #ff5f8f; --c2: #ff2e63; --c3: #ff8a5b; --border: #ffe3ec; }
.detail.theme-recruit { --c1: #4d7dff; --c2: #2b5cf6; --c3: #7b5bff; --border: #dce6ff; }
.d-container { max-width: 860px; margin: 0 auto; padding: 0 20px 50px; }
.d-hero { color: #fff; text-align: center; padding: 56px 20px 44px;
  background: linear-gradient(135deg, var(--c1) 0%, var(--c2) 45%, var(--c3) 100%); }
.d-badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px; border-radius: 20px;
  background: rgba(255,255,255,.18); font-size: 13px; letter-spacing: 1px; }
.d-hero h1 { font-size: 32px; font-weight: 800; margin: 18px 0 10px; text-shadow: 0 4px 18px rgba(0,0,0,.18); }
.d-sub { font-size: 15px; opacity: .95; margin: 0; }
.d-block { margin-top: 44px; }
.d-title { font-size: 21px; font-weight: 800; color: #22223a; line-height: 1.6;
  border-left: 4px solid var(--c2); padding-left: 14px; margin: 0 0 18px; }
.d-para { font-size: 16px; line-height: 2; text-indent: 2em; color: #44445a; margin: 14px 0; text-align: justify; }
.d-actions { display: flex; gap: 14px; justify-content: center; margin-top: 48px; flex-wrap: wrap; }
.d-btn { display: inline-flex; align-items: center; gap: 6px; padding: 12px 28px; border-radius: 30px;
  font-size: 15px; font-weight: bold; text-decoration: none; cursor: pointer; transition: all .25s; }
.d-btn-primary { background: linear-gradient(135deg, var(--c1), var(--c2)); color: #fff;
  box-shadow: 0 8px 20px rgba(0,0,0,.15); }
.d-btn-primary:hover { transform: translateY(-2px); }
.d-btn-ghost { border: 1.5px solid var(--c2); color: var(--c2); }
.d-btn-ghost:hover { background: var(--c2); color: #fff; }
.d-footer { background: #22223a; color: #8a8a9a; text-align: center; padding: 30px 20px; font-size: 12px; line-height: 1.8; }
.d-foot-brand { font-size: 17px; font-weight: bold; color: #fff; letter-spacing: 2px; margin-bottom: 10px; }
</style>