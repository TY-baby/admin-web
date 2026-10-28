<!-- 新文件：D:\work\project\hywork\project\hytf\hytf-web\src\views\public\NewsDetail.vue -->
<template>
  <div class="news-page">
    <header class="np-hero">
      <div class="np-badge"><i class="el-icon-news"></i> 新闻资讯</div>
      <h1>{{ item.title }}</h1>
      <p class="np-meta">发布日期：{{ item.date }}　来源：{{ item.source }}</p>
    </header>
    <main class="np-container">
      <p class="np-para" v-for="(p, i) in item.paras" :key="i">{{ p }}</p>
      <div class="np-actions">
        <a class="np-btn" href="javascript:;" @click="back"><i class="el-icon-back"></i> 返回</a>
      </div>
    </main>
    <footer class="np-footer">版权声明：转载此文是出于传递更多信息之目的。广告内容请自行辨别，本站不参与任何推荐与导购。</footer>
  </div>
</template>

<script>
import { NEWS_LIST } from './promoNews'

export default {
  name: 'NewsDetail',
  computed: {
    idx() { return Number(this.$route.params.idx || 0) },
    item() { return NEWS_LIST[this.idx] || NEWS_LIST[0] }
  },
  methods: { back() { this.$router.go(-1) } }
}
</script>

<style scoped lang="scss">
.news-page { font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif; color: #2c2c3a; background: #fff; min-height: 100%; }
.np-hero { color: #fff; text-align: center; padding: 56px 20px 40px;
  background: linear-gradient(135deg, #ff5f8f 0%, #ff2e63 45%, #ff8a5b 100%); }
.np-badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px; border-radius: 20px;
  background: rgba(255,255,255,.18); font-size: 13px; letter-spacing: 1px; }
.np-hero h1 { font-size: 28px; font-weight: 800; margin: 18px auto 12px; max-width: 760px; line-height: 1.5;
  text-shadow: 0 4px 18px rgba(0,0,0,.18); }
.np-meta { font-size: 13px; opacity: .92; margin: 0; }
.np-container { max-width: 860px; margin: 0 auto; padding: 40px 20px 50px; }
.np-para { font-size: 16px; line-height: 2; text-indent: 2em; color: #44445a; margin: 14px 0; text-align: justify; }
.np-actions { text-align: center; margin-top: 40px; }
.np-btn { display: inline-flex; align-items: center; gap: 6px; padding: 12px 28px; border-radius: 30px;
  font-size: 15px; font-weight: bold; text-decoration: none; cursor: pointer;
  background: linear-gradient(135deg, #ff5f8f, #ff2e63); color: #fff; box-shadow: 0 8px 20px rgba(0,0,0,.15); }
.np-btn:hover { transform: translateY(-2px); }
.np-footer { background: #22223a; color: #8a8a9a; text-align: center; padding: 24px 20px; font-size: 12px; line-height: 1.8; }
</style>