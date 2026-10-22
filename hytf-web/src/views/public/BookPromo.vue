<template>
  <div class="promo">
    <header class="hero">
      <div class="hero-bg"></div>
      <div class="hero-inner">
        <div class="badge"><i class="el-icon-medal"></i> 官方认证 · 恒耀互娱</div>
        <h1 class="title">深度布局网文推广赛道<br />「平台 + 运营」双引擎驱动创作者价值</h1>
        <p class="subtitle">直播工会宣传 · 招聘宣传 — 覆盖内容分发、数据追踪与结算服务的全链路推广能力，助力优质内容精准触达目标读者。</p>
        <div class="cta">
          <a class="btn btn-primary" href="#join"><i class="el-icon-s-promotion"></i> 立即合作</a>
          <a class="btn btn-ghost" href="#about"><i class="el-icon-info"></i> 了解详情</a>
        </div>
        <div class="hero-stats">
          <div class="hs"><div class="hs-num">{{ displayReads }}</div><div class="hs-lbl">页面阅读量</div></div>
          <div class="hs"><div class="hs-num">5+</div><div class="hs-lbl">合作投放平台</div></div>
          <div class="hs"><div class="hs-num">T+1</div><div class="hs-lbl">数据结算周期</div></div>
        </div>
      </div>
    </header>

    <main class="container">
      <section id="about" class="section">
        <div class="sec-head">
          <span class="sec-tag">ABOUT US</span>
          <h2>关于恒耀互娱</h2>
          <p>恒耀互娱以「平台 + 运营」双引擎模式，为创作者与主播提供从曝光、引流到结算的一体化服务，数据透明可查、效果稳定可控。</p>
        </div>
        <div class="cards">
          <div class="card" v-for="f in features" :key="f.title">
            <div class="card-ico"><i :class="f.icon"></i></div>
            <div class="card-title">{{ f.title }}</div>
            <div class="card-desc">{{ f.desc }}</div>
          </div>
        </div>
      </section>

      <section id="join" class="section alt">
        <div class="sec-head">
          <span class="sec-tag">JOIN US</span>
          <h2>招募与合作方向</h2>
          <p>无论你是内容创作者、主播，还是寻求推广合作的伙伴，这里都有适合你的位置。</p>
        </div>
        <div class="join-grid">
          <div class="join-card">
            <div class="join-ico"><i class="el-icon-microphone"></i></div>
            <h3>直播工会宣传</h3>
            <ul>
              <li>专业运营团队一对一扶持</li>
              <li>流量资源与曝光位倾斜</li>
              <li>阶梯式分成，结算透明</li>
              <li>数据看板实时追踪效果</li>
            </ul>
          </div>
          <div class="join-card">
            <div class="join-ico"><i class="el-icon-s-custom"></i></div>
            <h3>招聘宣传</h3>
            <ul>
              <li>主播 / 运营 / 推广多岗位开放</li>
              <li>弹性工作时间，收入上不封顶</li>
              <li>系统化培训与晋升通道</li>
              <li>优质团队氛围与资源支持</li>
            </ul>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="sec-head">
          <span class="sec-tag">PROCESS</span>
          <h2>合作流程</h2>
        </div>
        <div class="steps">
          <div class="step" v-for="(s, i) in steps" :key="s">
            <div class="step-no">{{ i + 1 }}</div>
            <div class="step-txt">{{ s }}</div>
            <i v-if="i < steps.length - 1" class="el-icon-right step-arrow"></i>
          </div>
        </div>
      </section>

      <section class="cta-band">
        <h3>准备好开启你的推广之旅了吗？</h3>
        <p>联系官方客服，获取专属投放方案与结算说明。</p>
        <a class="btn btn-light" href="#about"><i class="el-icon-service"></i> 联系客服咨询</a>
      </section>
    </main>

    <footer class="footer">
      <div class="container">
        <div class="foot-brand">恒耀互娱 · HYTF</div>
        <p class="foot-meta">
          <span v-if="dateStr">发布日期：{{ dateStr }}</span>
          <span>来源：恒耀互娱官方</span>
          <span>阅读量：{{ displayReads }}</span>
        </p>
        <p class="foot-note">版权声明：转载此文是出于传递更多信息之目的。广告内容请自行辨别，本站不参与任何推荐与导购。</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'BookPromo',
  data() {
    return {
      reads: 0, displayReads: 0, dateStr: '', promoContent: '',
      features: [
        { icon: 'el-icon-data-line', title: '数据可视化', desc: '投放效果实时追踪，阅读量、转化率一目了然，决策有据可依。' },
        { icon: 'el-icon-coin', title: '结算透明', desc: '阶段性结算依据清晰，分成规则公开，收益按时到账。' },
        { icon: 'el-icon-aim', title: '精准触达', desc: '基于实时数据反馈持续优化投放策略，让优质内容找到对的人。' },
        { icon: 'el-icon-service', title: '运营扶持', desc: '专业运营团队全程陪跑，从内容到推广提供全链路支持。' }
      ],
      steps: ['提交合作意向', '专属方案匹配', '签约并投放', '数据追踪优化', '阶段结算收益']
    }
  },
  computed: {
    code() { return this.$route.params.code }
  },
  mounted() { this.loadVisit() },
  methods: {
    loadVisit() {
      const base = (process.env.VUE_APP_API_BASE || '') + '/api/v1/public/novel_promo/'
      fetch(base + encodeURIComponent(this.code))
          .then(r => r.json())
          .then(d => {
            if (d && d.code === 0 && d.data) {
              this.reads = Number(d.data.reads || 0)
              this.dateStr = d.data.date || ''
              this.promoContent = d.data.promo_content || ''
              this.animateReads()
            }
          })
          .catch(() => {})
    },
    animateReads() {
      const target = this.reads
      const dur = 900
      const t0 = Date.now()
      const tick = () => {
        const p = Math.min(1, (Date.now() - t0) / dur)
        this.displayReads = Math.floor(target * (1 - Math.pow(1 - p, 3)))
        if (p < 1) requestAnimationFrame(tick)
        else this.displayReads = target
      }
      tick()
    }
  }
}
</script>

<style scoped lang="scss">
.promo { font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif; color: #2c2c3a; background: #fff; }
.container { max-width: 1080px; margin: 0 auto; padding: 0 20px; }

.hero { position: relative; overflow: hidden; color: #fff;
  background: linear-gradient(135deg, #ff5f8f 0%, #ff2e63 45%, #ff8a5b 100%); }
.hero-bg { position: absolute; inset: 0;
  background:
      radial-gradient(circle at 15% 20%, rgba(255,255,255,.25), transparent 40%),
      radial-gradient(circle at 85% 30%, rgba(255,255,255,.18), transparent 42%); }
.hero-inner { position: relative; max-width: 1080px; margin: 0 auto; padding: 70px 20px 54px; text-align: center; }
.badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px; border-radius: 20px;
  background: rgba(255,255,255,.18); backdrop-filter: blur(4px); font-size: 13px; letter-spacing: 1px; }
.title { font-size: 38px; line-height: 1.35; font-weight: 800; margin: 20px 0 14px; text-shadow: 0 4px 18px rgba(0,0,0,.18); }
.subtitle { font-size: 16px; line-height: 1.9; max-width: 720px; margin: 0 auto 26px; opacity: .95; }
.cta { display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; }
.btn { display: inline-flex; align-items: center; gap: 6px; padding: 12px 28px; border-radius: 30px;
  font-size: 15px; font-weight: bold; text-decoration: none; transition: all .25s; cursor: pointer; }
.btn-primary { background: #fff; color: #ff2e63; box-shadow: 0 8px 20px rgba(0,0,0,.18); }
.btn-primary:hover { transform: translateY(-2px); }
.btn-ghost { border: 1.5px solid rgba(255,255,255,.8); color: #fff; }
.btn-ghost:hover { background: rgba(255,255,255,.15); }
.btn-light { background: #fff; color: #ff2e63; }
.hero-stats { display: flex; justify-content: center; gap: 48px; margin-top: 44px; flex-wrap: wrap; }
.hs-num { font-size: 32px; font-weight: 800; }
.hs-lbl { font-size: 13px; opacity: .9; margin-top: 4px; }

.section { padding: 60px 0; }
.section.alt { background: #fff6f8; }
.sec-head { text-align: center; max-width: 720px; margin: 0 auto 40px; }
.sec-tag { display: inline-block; font-size: 12px; letter-spacing: 3px; color: #ff2e63; font-weight: bold; }
.sec-head h2 { font-size: 28px; font-weight: 800; margin: 10px 0 12px; color: #22223a; }
.sec-head p { font-size: 15px; line-height: 1.9; color: #6b6b7b; }

.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.card { background: #fff; border: 1px solid #ffe3ec; border-radius: 14px; padding: 26px 20px; text-align: center;
  box-shadow: 0 6px 20px rgba(255,46,99,.06); transition: transform .25s, box-shadow .25s; }
.card:hover { transform: translateY(-6px); box-shadow: 0 14px 30px rgba(255,46,99,.14); }
.card-ico { width: 56px; height: 56px; line-height: 56px; margin: 0 auto 14px; border-radius: 50%;
  background: linear-gradient(135deg, #ff5f8f, #ff2e63); color: #fff; font-size: 26px; }
.card-title { font-size: 16px; font-weight: bold; margin-bottom: 8px; }
.card-desc { font-size: 13px; line-height: 1.8; color: #77778a; }

.join-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
.join-card { background: #fff; border-radius: 16px; padding: 32px 28px; box-shadow: 0 8px 26px rgba(255,46,99,.08); }
.join-ico { width: 60px; height: 60px; line-height: 60px; text-align: center; border-radius: 16px; font-size: 28px;
  background: linear-gradient(135deg, #ff8a5b, #ff2e63); color: #fff; margin-bottom: 16px; }
.join-card h3 { font-size: 20px; font-weight: 800; margin: 0 0 14px; }
.join-card ul { margin: 0; padding-left: 20px; color: #5c5c6e; font-size: 14px; line-height: 2.1; }

.steps { display: flex; align-items: center; justify-content: center; gap: 10px; flex-wrap: wrap; }
.step { display: flex; align-items: center; gap: 10px; }
.step-no { width: 38px; height: 38px; line-height: 38px; text-align: center; border-radius: 50%; font-weight: bold;
  background: linear-gradient(135deg, #ff5f8f, #ff2e63); color: #fff; }
.step-txt { font-size: 14px; font-weight: 600; color: #44445a; }
.step-arrow { color: #ffb3c6; font-size: 18px; margin: 0 6px; }

.cta-band { text-align: center; padding: 54px 20px; border-radius: 18px; color: #fff;
  background: linear-gradient(135deg, #ff5f8f 0%, #ff2e63 100%); }
.cta-band h3 { font-size: 24px; font-weight: 800; margin: 0 0 10px; }
.cta-band p { opacity: .95; margin: 0 0 22px; }

.footer { background: #22223a; color: #b8b8c8; padding: 34px 0; text-align: center; }
.foot-brand { font-size: 18px; font-weight: bold; color: #fff; letter-spacing: 2px; }
.foot-meta { font-size: 13px; margin: 12px 0; span { margin: 0 12px; } }
.foot-note { font-size: 12px; color: #8a8a9a; line-height: 1.8; max-width: 720px; margin: 0 auto; }

@media (max-width: 860px) {
  .cards { grid-template-columns: repeat(2, 1fr); }
  .join-grid { grid-template-columns: 1fr; }
  .title { font-size: 28px; }
  .hero-stats { gap: 28px; }
}
</style>