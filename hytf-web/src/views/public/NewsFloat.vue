<!-- 新文件：D:\work\project\hywork\project\hytf\hytf-web\src\views\public\NewsFloat.vue -->
<template>
  <div class="news-float" :class="theme">
    <div class="nf-head"><i class="el-icon-bell"></i> 最新资讯<span class="nf-more">共{{ list.length }}条</span></div>
    <ul class="nf-list" ref="list" @mouseenter="pause = true" @mouseleave="pause = false">
      <li v-for="(n, i) in list" :key="i" @click="go(i)">
        <span class="nf-date">{{ n.date }} · {{ n.source }}</span>
        <span class="nf-title">{{ n.title }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { NEWS_LIST } from './promoNews'

export default {
  name: 'NewsFloat',
  props: { theme: { type: String, default: 'theme-union' } },
  data() { return { pause: false, timer: null } },
  computed: { list() { return NEWS_LIST } },
  mounted() {
    this.timer = setInterval(() => {
      if (this.pause) return
      const el = this.$refs.list
      if (!el || el.scrollHeight <= el.clientHeight) return
      if (el.scrollTop + el.clientHeight >= el.scrollHeight - 1) el.scrollTop = 0
      else el.scrollTop += 1
    }, 60)
  },
  beforeDestroy() { clearInterval(this.timer) },
  methods: { go(i) { this.$router.push('/news/' + i) } }
}
</script>

<style scoped lang="scss">
.news-float { position: fixed; right: 22px; top: 50%; transform: translateY(-50%); width: 450px; z-index: 999;
  background: #fff; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,.15); overflow: hidden;
  border: 1px solid var(--border);
  --c1: #ff5f8f; --c2: #ff2e63; --c3: #ff8a5b; --border: #ffe3ec; }
.news-float.theme-recruit { --c1: #4d7dff; --c2: #2b5cf6; --c3: #7b5bff; --border: #dce6ff; }
.nf-head { display: flex; align-items: center; gap: 6px; padding: 10px 14px; color: #fff;
  font-weight: bold; font-size: 14px; background: linear-gradient(135deg, var(--c1), var(--c2)); }
.nf-more { margin-left: auto; font-size: 12px; opacity: .9; font-weight: normal; }
.nf-list { list-style: none; margin: 0; padding: 0; height: 470px; overflow-y: auto; }
.nf-list li { padding: 8px 14px; border-bottom: 1px dashed #eee; cursor: pointer; transition: background .2s; }
.nf-list li:last-child { border-bottom: none; }
.nf-list li:hover { background: #f7f8fc; }
.nf-date { display: block; font-size: 12px; color: #999; margin-bottom: 3px; }
.nf-title { display: block; font-size: 13px; color: #333; line-height: 20px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.nf-list::-webkit-scrollbar { width: 4px; }
.nf-list::-webkit-scrollbar-thumb { background: #d8d8e2; border-radius: 2px; }
@media (max-width: 860px) {
  .news-float { width: 300px; right: 10px; }
  .nf-list { height: 324px; }
}
</style>