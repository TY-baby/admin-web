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
@import './PromoDetail.vue';
</style>