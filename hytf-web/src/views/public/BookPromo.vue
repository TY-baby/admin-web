<template>
  <div class="promo" :class="c.theme">
    <header class="hero">
      <div class="hero-bg"></div>
      <div class="hero-inner">
        <div class="badge"><i class="el-icon-medal"></i> {{ c.badge }}</div>
        <h1 class="title" v-html="fill(c.title)"></h1>
        <p class="subtitle">{{ c.subtitle }}</p>
        <div class="cta">
          <a class="btn btn-primary" href="javascript:;" @click="openContact"><i class="el-icon-s-promotion"></i> 立即合作</a>
          <a class="btn btn-ghost" href="javascript:;" @click="goDetail"><i class="el-icon-info"></i> 了解详情</a>
        </div>
        <div class="hero-stats">
          <div class="hs"><div class="hs-num">{{ displayReads }}</div><div class="hs-lbl">页面阅读量</div></div>
          <div class="hs" v-for="s in c.stats" :key="s.lbl">
            <div class="hs-num">{{ s.num }}</div><div class="hs-lbl">{{ s.lbl }}</div>
          </div>
        </div>
      </div>
    </header>

    <main class="container">
      <section id="about" class="section">
        <div class="sec-head">
          <span class="sec-tag">ABOUT US</span>
          <h2>关于{{ company }}</h2>
          <p>{{ company }}以「平台 + 运营」双引擎模式，为创作者、主播与求职者提供从曝光、引流到结算/成长的一体化服务，数据透明可查、效果稳定可控。</p>
        </div>
        <div class="cards">
          <div class="card" v-for="(f, i) in c.features" :key="f.title" @click="goModule(i)" style="cursor:pointer">
            <div class="card-ico"><i :class="f.icon"></i></div>
            <div class="card-title">{{ f.title }}</div>
            <div class="card-desc">{{ f.desc }}</div>
          </div>
        </div>
      </section>

      <section id="join" class="section alt">
        <div class="sec-head">
          <span class="sec-tag">JOIN US</span>
          <h2>{{ c.joinTitle }}</h2>
          <p>{{ fill(c.joinDesc) }}</p>
        </div>
        <div class="points">
          <div class="point" v-for="p in c.points" :key="p">
            <i class="el-icon-check"></i><span>{{ p }}</span>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="sec-head">
          <span class="sec-tag">PROCESS</span>
          <h2>{{ c.processTitle }}</h2>
        </div>
        <div class="steps">
          <div class="step" v-for="(s, i) in c.steps" :key="s">
            <div class="step-no">{{ i + 1 }}</div>
            <div class="step-txt">{{ s }}</div>
            <i v-if="i < c.steps.length - 1" class="el-icon-right step-arrow"></i>
          </div>
        </div>
      </section>

      <section class="cta-band">
        <h3>{{ c.ctaTitle }}</h3>
        <p>{{ c.ctaDesc }}</p>
      </section>
    </main>

    <footer class="footer">
      <div class="container">
        <div class="foot-brand">{{ company }} · HYTF</div>
        <p class="foot-meta">
          <span v-if="dateStr">发布日期：{{ dateStr }}</span>
          <span>来源：{{ company }}官方</span>
          <span>阅读量：{{ displayReads }}</span>
        </p>
        <p class="foot-note">版权声明：转载此文是出于传递更多信息之目的。广告内容请自行辨别，本站不参与任何推荐与导购。</p>
      </div>
    </footer>

    <el-dialog title="合作联系" :visible.sync="contactVisible" width="420px">
      <div class="contact-box">
        <div class="c-item"><span class="c-lbl">客户名称</span><span class="c-val">{{ company }}</span></div>
        <div class="c-item"><span class="c-lbl">联系方式</span><span class="c-val">{{ phone || '暂未提供' }}</span></div>
      </div>
      <span slot="footer"><el-button type="primary" @click="contactVisible = false">我知道了</el-button></span>
    </el-dialog>
  </div>
</template>

<script>
const UNION = {
  theme: 'theme-union',
  badge: '官方认证 · 直播工会宣传',
  title: '{company}直播工会招募<br />专业运营护航 · 流量资源倾斜',
  subtitle: '面向主播与工会的一站式直播推广合作，提供曝光扶持、运营陪跑与透明结算，助力直播事业稳步增长。',
  stats: [{ num: '5+', lbl: '合作直播平台' }, { num: 'T+1', lbl: '结算周期' }, { num: '1对1', lbl: '运营扶持' }],
  features: [
    { icon: 'el-icon-microphone', title: '主播孵化', desc: '从0到1系统化培养，专业导师全程陪跑，快速提升直播能力。' },
    { icon: 'el-icon-data-line', title: '流量扶持', desc: '优质曝光位与流量资源倾斜，让每一场直播都被更多人看见。' },
    { icon: 'el-icon-coin', title: '阶梯分成', desc: '分成规则公开透明，收益阶梯递增，多劳多得按时结算。' },
    { icon: 'el-icon-service', title: '运营陪跑', desc: '专属运营团队对接，选题、话术、活动策划全方位支持。' }
  ],
  joinTitle: '工会合作权益',
  joinDesc: '加入{company}直播工会，享受从资源到运营的全方位扶持。',
  points: ['专业运营团队一对一扶持', '流量资源与首页曝光位倾斜', '阶梯式分成，结算透明及时',
    '数据看板实时追踪直播效果', '活动策划与 PK 资源对接'],
  processTitle: '合作流程',
  steps: ['提交合作意向', '资质沟通匹配', '签约入驻', '直播运营扶持', '阶段结算收益'],
  ctaTitle: '准备好开启你的直播之旅了吗？',
  ctaDesc: '联系官方客服，获取专属工会合作方案与分成说明。'
}
const RECRUIT = {
  theme: 'theme-recruit',
  badge: '官方认证 · 招聘宣传',
  title: '{company}诚聘英才<br />多岗位开放 · 收入上不封顶',
  subtitle: '我们正在寻找热爱内容、渴望成长的你。主播、运营、推广多岗位开放，弹性工作、系统培训、晋升透明。',
  stats: [{ num: '多', lbl: '在招岗位' }, { num: '弹性', lbl: '工作时间' }, { num: '上不封顶', lbl: '收入空间' }],
  features: [
    { icon: 'el-icon-s-custom', title: '主播', desc: '形象佳、表达力强，热爱镜头，负责日常直播与粉丝互动。' },
    { icon: 'el-icon-setting', title: '运营', desc: '负责内容策划、数据分析与账号运营，推动直播效果增长。' },
    { icon: 'el-icon-share', title: '推广', desc: '负责渠道拓展与投放执行，具备较强的沟通与执行力。' },
    { icon: 'el-icon-trophy', title: '晋升通道', desc: '完善的培训体系与清晰的晋升路径，让每一分努力被看见。' }
  ],
  joinTitle: '岗位福利',
  joinDesc: '我们提供有竞争力的待遇与成长空间，期待你的加入。',
  points: ['主播 / 运营 / 推广多岗位开放', '弹性工作时间，收入上不封顶', '系统化培训与清晰晋升通道',
    '优质团队氛围与资源支持', '五险一金与节日福利'],
  processTitle: '应聘流程',
  steps: ['投递简历', '简历初筛', '面试沟通', 'offer 发放', '入职培训'],
  ctaTitle: '准备好开启你的职业新篇章了吗？',
  ctaDesc: '联系官方客服，获取在招岗位详情与投递方式。'
}

export default {
  name: 'BookPromo',
  data() {
    return { reads: 0, displayReads: 0, dateStr: '', promoContent: '',
      company: '', phone: '', contactVisible: false }
  },
  computed: {
    code() { return this.$route.params.code },
    isRecruit() { return this.promoContent === '招聘宣传' },
    c() { return this.isRecruit ? RECRUIT : UNION }
  },
  mounted() { this.loadVisit() },
  methods: {
    fill(t) { return String(t || '').replace(/\{company\}/g, this.company) },
    openContact() { this.contactVisible = true },
    goDetail() { this.$router.push('/book/' + this.code + '/detail') },
    goModule(i) { this.$router.push('/book/' + this.code + '/module/' + i) },
    loadVisit() {
      const base = (process.env.VUE_APP_API_BASE || '') + '/api/v1/public/novel_promo/'
      fetch(base + encodeURIComponent(this.code))
          .then(r => r.json())
          .then(d => {
            if (d && d.code === 0 && d.data) {
              this.reads = Number(d.data.reads || 0)
              this.dateStr = d.data.date || ''
              this.promoContent = d.data.promo_content || ''
              this.company = d.data.company_name || ''
              this.phone = d.data.phone || ''
              if (this.company) document.title = this.company
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
.promo { font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif; color: #2c2c3a; background: #fff;
  --c1: #ff5f8f; --c2: #ff2e63; --c3: #ff8a5b; --alt: #fff6f8; --border: #ffe3ec; }
.promo.theme-recruit { --c1: #4d7dff; --c2: #2b5cf6; --c3: #7b5bff; --alt: #f2f6ff; --border: #dce6ff; }
.container { max-width: 1080px; margin: 0 auto; padding: 0 20px; }

.hero { position: relative; overflow: hidden; color: #fff;
  background: linear-gradient(135deg, var(--c1) 0%, var(--c2) 45%, var(--c3) 100%); }
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
.btn-primary { background: #fff; color: var(--c2); box-shadow: 0 8px 20px rgba(0,0,0,.18); }
.btn-primary:hover { transform: translateY(-2px); }
.btn-ghost { border: 1.5px solid rgba(255,255,255,.8); color: #fff; }
.btn-ghost:hover { background: rgba(255,255,255,.15); }
.btn-light { background: #fff; color: var(--c2); }
.hero-stats { display: flex; justify-content: center; gap: 48px; margin-top: 44px; flex-wrap: wrap; }
.hs-num { font-size: 32px; font-weight: 800; }
.hs-lbl { font-size: 13px; opacity: .9; margin-top: 4px; }

.section { padding: 60px 0; }
.section.alt { background: var(--alt); }
.sec-head { text-align: center; max-width: 720px; margin: 0 auto 40px; }
.sec-tag { display: inline-block; font-size: 12px; letter-spacing: 3px; color: var(--c2); font-weight: bold; }
.sec-head h2 { font-size: 28px; font-weight: 800; margin: 10px 0 12px; color: #22223a; }
.sec-head p { font-size: 15px; line-height: 1.9; color: #6b6b7b; }

.cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.card { background: #fff; border: 1px solid var(--border); border-radius: 14px; padding: 26px 20px; text-align: center;
  box-shadow: 0 6px 20px rgba(0,0,0,.05); transition: transform .25s, box-shadow .25s; }
.card:hover { transform: translateY(-6px); box-shadow: 0 14px 30px rgba(0,0,0,.12); }
.card-ico { width: 56px; height: 56px; line-height: 56px; margin: 0 auto 14px; border-radius: 50%;
  background: linear-gradient(135deg, var(--c1), var(--c2)); color: #fff; font-size: 26px; }
.card-title { font-size: 16px; font-weight: bold; margin-bottom: 8px; }
.card-desc { font-size: 13px; line-height: 1.8; color: #77778a; }

.points { max-width: 720px; margin: 0 auto; display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.point { display: flex; align-items: center; gap: 10px; background: #fff; border: 1px solid var(--border);
  border-radius: 12px; padding: 16px 18px; font-size: 15px; color: #44445a; font-weight: 600; }
.point i { color: var(--c2); font-size: 18px; font-weight: bold; }

.steps { display: flex; align-items: center; justify-content: center; gap: 10px; flex-wrap: wrap; }
.step { display: flex; align-items: center; gap: 10px; }
.step-no { width: 38px; height: 38px; line-height: 38px; text-align: center; border-radius: 50%; font-weight: bold;
  background: linear-gradient(135deg, var(--c1), var(--c2)); color: #fff; }
.step-txt { font-size: 14px; font-weight: 600; color: #44445a; }
.step-arrow { color: var(--c1); font-size: 18px; margin: 0 6px; opacity: .6; }

.cta-band { text-align: center; padding: 54px 20px; border-radius: 18px; color: #fff;
  background: linear-gradient(135deg, var(--c1) 0%, var(--c2) 100%); }
.cta-band h3 { font-size: 24px; font-weight: 800; margin: 0 0 10px; }
.cta-band p { opacity: .95; margin: 0 0 22px; }

.footer { background: #22223a; color: #b8b8c8; padding: 34px 0; text-align: center; }
.foot-brand { font-size: 18px; font-weight: bold; color: #fff; letter-spacing: 2px; }
.foot-meta { font-size: 13px; margin: 12px 0; span { margin: 0 12px; } }
.foot-note { font-size: 12px; color: #8a8a9a; line-height: 1.8; max-width: 720px; margin: 0 auto; }

.contact-box { padding: 6px 4px; }
.c-item { display: flex; align-items: center; padding: 12px 0; border-bottom: 1px dashed #eee; font-size: 15px; }
.c-item:last-child { border-bottom: none; }
.c-lbl { width: 90px; color: #888; flex-shrink: 0; }
.c-val { font-weight: bold; color: #333; }

@media (max-width: 860px) {
  .cards { grid-template-columns: repeat(2, 1fr); }
  .points { grid-template-columns: 1fr; }
  .title { font-size: 28px; }
  .hero-stats { gap: 28px; }
}
</style>
