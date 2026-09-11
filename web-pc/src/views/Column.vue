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

    <div class="container col-wrap">
      <h1>{{ content.title }}</h1>
      <p class="desc">{{ content.desc }}</p>
      <div class="cards">
        <div v-for="c in content.items" :key="c.title" class="card" @click="onClick(c)">
          <div class="ico">{{ c.icon }}</div>
          <h3>{{ c.title }}</h3>
          <p>{{ c.text }}</p>
          <span class="link" v-if="c.url">了解详情 →</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { openAndTrack } from '@/utils/track'

const COLUMNS = {
  about: {
    title: '关于我们',
    desc: 'Base Room 致力于为企业提供数字化推流与数据洞察服务，让每一次点击都产生价值。',
    items: [
      { icon: '🏢', title: '公司简介', text: '成立于数字化浪潮之中，专注企业流量运营与数据服务。', url: 'https://www.base-room.cn/about' },
      { icon: '🎖️', title: '发展历程', text: '多年深耕行业，累计服务上千家企业客户。', url: 'https://www.base-room.cn/history' },
      { icon: '🤝', title: '企业文化', text: '以客户为中心，用数据驱动增长，以技术赢得信任。', url: 'https://www.base-room.cn/culture' }
    ]
  },
  product: {
    title: '产品中心',
    desc: '覆盖官网建设、推流运营、数据分析的全套数字化产品矩阵。',
    items: [
      { icon: '🌐', title: '官网建站', text: '响应式企业官网，多端自适应，快速上线。', url: 'https://www.base-room.cn/p/site' },
      { icon: '📈', title: '推流引擎', text: '智能流量分发与点击转化全链路追踪。', url: 'https://www.base-room.cn/p/push' },
      { icon: '📊', title: '数据大屏', text: '实时可视化业务全貌，一屏掌握关键指标。', url: 'https://www.base-room.cn/p/screen' }
    ]
  },
  contact: {
    title: '联系我们',
    desc: '期待与您合作，欢迎随时通过以下方式联系我们。',
    items: [
      { icon: '📞', title: '客服热线', text: '400-000-0000（工作日 9:00 - 18:00）', url: '' },
      { icon: '✉️', title: '商务邮箱', text: 'business@base-room.cn', url: '' },
      { icon: '📍', title: '公司地址', text: '中国 · 数字化产业基地 A 座 18 层', url: '' }
    ]
  }
}

export default {
  name: 'ColumnPage',
  data() {
    return { content: { title: '', desc: '', items: [] } }
  },
  created() { this.load() },
  watch: {
    '$route.params.column'() { this.load() }
  },
  methods: {
    load() {
      this.content = COLUMNS[this.$route.params.column] || COLUMNS.about
    },
    onClick(c) {
      openAndTrack({ title: this.content.title + '-' + c.title, fee: 0, url: c.url, id: 0 })
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar { background: #fff; border-bottom: 1px solid #eef2f7; position: sticky; top: 0; z-index: 100; }
.nav-inner { display: flex; align-items: center; justify-content: space-between; height: 66px; }
.logo { display: flex; align-items: center; gap: 10px; font-size: 20px; font-weight: 800; color: #0f172a; cursor: pointer; }
.back { color: #2563eb; font-size: 14px; cursor: pointer; }
.col-wrap { padding: 48px 20px 80px; }
.col-wrap h1 { font-size: 30px; font-weight: 800; margin-bottom: 12px; }
.desc { color: #64748b; font-size: 15px; margin-bottom: 36px; line-height: 1.8; }
.cards { display: grid; grid-template-columns: repeat(3,1fr); gap: 24px; }
.card { background: #fff; border: 1px solid #eef2f7; border-radius: 16px; padding: 32px 24px; cursor: pointer; transition: all .3s; }
.card:hover { transform: translateY(-6px); box-shadow: 0 18px 44px rgba(15,23,42,.08); border-color: #bfdbfe; }
.ico { font-size: 38px; margin-bottom: 16px; }
.card h3 { font-size: 18px; margin-bottom: 10px; color: #0f172a; }
.card p { font-size: 13px; color: #94a3b8; line-height: 1.75; margin-bottom: 14px; }
.link { font-size: 13px; color: #2563eb; font-weight: 600; }
@media (max-width: 900px) { .cards { grid-template-columns: 1fr; } }
</style>