<template>
  <div class="login-page">
    <!-- ===== 科技感动态背景 ===== -->
    <div class="bg-grid"></div>
    <div class="bg-glow glow-a"></div>
    <div class="bg-glow glow-b"></div>
    <div class="bg-scan"></div>
    <div class="bg-particles">
      <span v-for="n in 24" :key="n" :style="particleStyle(n)"></span>
    </div>
    <div class="bg-rings">
      <div class="ring r1"></div>
      <div class="ring r2"></div>
      <div class="ring r3"></div>
    </div>

    <!-- ===== 登录卡片 ===== -->
    <div class="login-card">
      <div class="card-head">
        <div class="logo">
          <svg viewBox="0 0 48 48" width="42" height="42">
            <circle cx="18" cy="24" r="12" fill="#22d3ee" opacity="0.85"/>
            <circle cx="30" cy="24" r="12" fill="#6366f1" opacity="0.85"/>
          </svg>
        </div>
        <h1 class="title">Base Room 推流后台</h1>
        <p class="subtitle">网站流量运营 · 点击数据实时洞察</p>
      </div>

      <el-form :model="form" :rules="rules" ref="form" @submit.native.prevent="handleLogin" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" prefix-icon="el-icon-user" />
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="form.password" :type="showPwd ? 'text' : 'password'" placeholder="请输入密码" prefix-icon="el-icon-lock">
            <i slot="suffix" :class="showPwd ? 'el-icon-open' : 'el-icon-turn-off'" class="pwd-eye" @click="showPwd = !showPwd"></i>
          </el-input>
        </el-form-item>

        <div class="form-options">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <span class="tips">默认 admin / 123456</span>
        </div>

        <el-button type="primary" native-type="submit" :loading="loading" class="login-btn">
          {{ loading ? '登录中...' : '登 录' }}
        </el-button>
      </el-form>

      <div class="card-foot">
        <span>© 2026 Base Room · www.base-room.cn</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      loading: false,
      showPwd: false,
      rememberMe: true,
      form: { username: 'admin', password: '123456' },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },
  methods: {
    particleStyle(n) {
      const size = Math.random() * 3 + 1
      const left = Math.random() * 100
      const delay = Math.random() * 8
      const duration = Math.random() * 10 + 10
      return {
        width: size + 'px',
        height: size + 'px',
        left: left + '%',
        animationDelay: delay + 's',
        animationDuration: duration + 's'
      }
    },
    handleLogin() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        this.loading = true
        this.$store.dispatch('user/login', this.form).then(() => {
          this.$message.success('登录成功')
          this.$router.push('/')
        }).catch(() => {}).finally(() => {
          this.loading = false
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  height: 100vh;
  width: 100vw;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(ellipse at 50% 0%, #12224a 0%, #070d1f 55%, #04070f 100%);
}

/* ===== 网格 ===== */
.bg-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(56,189,248,0.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(56,189,248,0.07) 1px, transparent 1px);
  background-size: 46px 46px;
  mask-image: radial-gradient(ellipse at center, #000 30%, transparent 78%);
  -webkit-mask-image: radial-gradient(ellipse at center, #000 30%, transparent 78%);
}

/* ===== 双色光晕 ===== */
.bg-glow { position: absolute; border-radius: 50%; filter: blur(90px); pointer-events: none; }
.glow-a {
  width: 620px; height: 620px; top: -18%; left: -10%;
  background: radial-gradient(circle, rgba(34,211,238,0.30) 0%, transparent 68%);
  animation: drift-a 16s ease-in-out infinite;
}
.glow-b {
  width: 560px; height: 560px; bottom: -22%; right: -8%;
  background: radial-gradient(circle, rgba(99,102,241,0.34) 0%, transparent 68%);
  animation: drift-b 19s ease-in-out infinite;
}
@keyframes drift-a { 0%,100% { transform: translate(0,0) } 50% { transform: translate(60px,44px) } }
@keyframes drift-b { 0%,100% { transform: translate(0,0) } 50% { transform: translate(-54px,-40px) } }

/* ===== 扫描光线 ===== */
.bg-scan {
  position: absolute; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, rgba(34,211,238,0.55), transparent);
  animation: scan 7s linear infinite;
  pointer-events: none;
}
@keyframes scan { 0% { top: -2% } 100% { top: 102% } }

/* ===== 上浮粒子 ===== */
.bg-particles { position: absolute; inset: 0; pointer-events: none; }
.bg-particles span {
  position: absolute; bottom: -12px;
  background: rgba(125,211,252,0.75);
  border-radius: 50%;
  box-shadow: 0 0 8px rgba(34,211,238,0.8);
  animation: float-up linear infinite;
}
@keyframes float-up {
  0%   { transform: translateY(0) scale(1); opacity: 0; }
  12%  { opacity: 1; }
  88%  { opacity: 1; }
  100% { transform: translateY(-108vh) scale(0.4); opacity: 0; }
}

/* ===== 科技圆环 ===== */
.bg-rings { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; pointer-events: none; }
.ring { position: absolute; border-radius: 50%; border: 1px solid rgba(56,189,248,0.16); }
.r1 { width: 520px; height: 520px; animation: spin 26s linear infinite; border-top-color: rgba(34,211,238,0.55); }
.r2 { width: 700px; height: 700px; animation: spin 38s linear infinite reverse; border-left-color: rgba(99,102,241,0.45); }
.r3 { width: 880px; height: 880px; animation: spin 52s linear infinite; border-bottom-color: rgba(56,189,248,0.30); }
@keyframes spin { from { transform: rotate(0deg) } to { transform: rotate(360deg) } }

/* ===== 登录卡片 ===== */
.login-card {
  position: relative; z-index: 10;
  width: 100%; max-width: 420px;
  padding: 44px 40px 30px;
  background: rgba(15,26,52,0.62);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(99,179,237,0.22);
  border-radius: 20px;
  box-shadow: 0 24px 70px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.07);
  animation: card-in .7s cubic-bezier(.22,1,.36,1);
}
@keyframes card-in { from { opacity: 0; transform: translateY(26px) } to { opacity: 1; transform: translateY(0) } }

.card-head { text-align: center; margin-bottom: 34px; }
.logo { margin-bottom: 16px; }
.logo svg { filter: drop-shadow(0 4px 18px rgba(34,211,238,0.55)); }
.title {
  font-size: 25px; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px;
  background: linear-gradient(135deg, #ffffff 20%, #7dd3fc 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.subtitle { font-size: 13px; color: rgba(148,197,255,0.72); letter-spacing: .5px; }

.login-form ::v-deep .el-form-item { margin-bottom: 22px; }
.login-form ::v-deep .el-input__inner {
  height: 46px; line-height: 46px;
  background: rgba(4,10,26,0.60);
  border: 1px solid rgba(99,179,237,0.22);
  color: #e6f1ff;
  border-radius: 10px;
}
.login-form ::v-deep .el-input__inner::placeholder { color: rgba(148,197,255,0.42); }
.login-form ::v-deep .el-input__inner:focus {
  border-color: #22d3ee;
  box-shadow: 0 0 0 3px rgba(34,211,238,0.14);
}
.login-form ::v-deep .el-input__icon { color: rgba(125,211,252,0.65); line-height: 46px; }
.pwd-eye { cursor: pointer; }
.pwd-eye:hover { color: #22d3ee; }

.form-options { display: flex; align-items: center; justify-content: space-between; margin-bottom: 26px; }
.form-options ::v-deep .el-checkbox__label { color: rgba(148,197,255,0.75); font-size: 13px; }
.form-options ::v-deep .el-checkbox__inner { background: rgba(4,10,26,0.6); border-color: rgba(99,179,237,0.35); }
.form-options ::v-deep .el-checkbox__input.is-checked .el-checkbox__inner { background: #22d3ee; border-color: #22d3ee; }
.tips { font-size: 12px; color: rgba(148,197,255,0.42); }

.login-btn {
  width: 100%; height: 48px; border-radius: 10px;
  font-size: 16px; font-weight: 700; letter-spacing: 4px;
  background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
  border: none !important;
  box-shadow: 0 10px 26px rgba(14,165,233,0.38);
  transition: all .28s;
}
.login-btn:hover { transform: translateY(-2px); box-shadow: 0 14px 34px rgba(99,102,241,0.5); }

.card-foot { margin-top: 26px; text-align: center; font-size: 11px; color: rgba(148,197,255,0.35); }

@media (max-width: 480px) {
  .login-card { max-width: calc(100% - 32px); padding: 36px 24px 24px; }
  .title { font-size: 21px; }
  .r2, .r3 { display: none; }
}
</style>