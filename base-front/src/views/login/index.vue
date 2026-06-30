<template>
  <div class="login-page" @mousemove="onMouseMove">
    <!-- 动态科技背景 -->
    <div class="bg-grid"></div>
    <div class="bg-glow"></div>
    <div class="bg-particles">
      <span v-for="n in 20" :key="n" :style="particleStyle(n)"></span>
    </div>

    <!-- 左侧 AI 数字人展示区 -->
    <div class="login-left">
      <div class="brand-area">
        <div class="logo">
          <svg viewBox="0 0 48 48" width="40" height="40">
            <circle cx="18" cy="24" r="12" fill="#4ADE80" opacity="0.85"/>
            <circle cx="30" cy="24" r="12" fill="#60A5FA" opacity="0.85"/>
          </svg>
        </div>
        <h1 class="brand-title">Base Room</h1>
        <p class="brand-sub">AI 驱动的企业数字化管理平台</p>
      </div>

      <!-- AI 数字人 -->
      <div class="ai-human" ref="aiHuman">
        <div class="ai-halo"></div>
        <div class="ai-halo delay"></div>

        <svg class="ai-body" viewBox="0 0 240 300" width="240" height="300">
          <defs>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#6366f1"/>
              <stop offset="100%" stop-color="#4f46e5"/>
            </linearGradient>
            <linearGradient id="faceGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#ffffff"/>
              <stop offset="100%" stop-color="#e0e7ff"/>
            </linearGradient>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>

          <!-- 身体 -->
          <ellipse cx="120" cy="260" rx="70" ry="22" fill="#312e81" opacity="0.3"/>
          <path d="M70 130 Q60 250 80 260 L160 260 Q180 250 170 130 Z" fill="url(#bodyGrad)" filter="url(#glow)"/>
          <path d="M85 150 Q80 240 95 245 L145 245 Q160 240 155 150 Z" fill="#4338ca" opacity="0.4"/>

          <!-- 脖子 -->
          <rect x="108" y="115" width="24" height="30" rx="6" fill="#818cf8"/>

          <!-- 头部 -->
          <circle cx="120" cy="80" r="55" fill="url(#faceGrad)" filter="url(#glow)"/>
          <path d="M70 60 Q120 30 170 60" stroke="#c7d2fe" stroke-width="3" fill="none" opacity="0.6"/>

          <!-- 耳朵/天线 -->
          <rect x="55" y="65" width="12" height="30" rx="6" fill="#6366f1"/>
          <rect x="173" y="65" width="12" height="30" rx="6" fill="#6366f1"/>
          <line x1="120" y1="25" x2="120" y2="5" stroke="#818cf8" stroke-width="3" stroke-linecap="round"/>
          <circle cx="120" cy="5" r="5" fill="#4ade80" filter="url(#glow)">
            <animate attributeName="opacity" values="1;0.4;1" dur="2s" repeatCount="indefinite"/>
          </circle>

          <!-- 眼睛 -->
          <g class="ai-eyes">
            <ellipse cx="98" cy="78" rx="14" ry="16" fill="#1e1b4b"/>
            <ellipse cx="142" cy="78" rx="14" ry="16" fill="#1e1b4b"/>
            <circle class="pupil" cx="98" cy="78" r="5" fill="#60a5fa" :style="pupilStyle(98, 78)"/>
            <circle class="pupil" cx="142" cy="78" r="5" fill="#60a5fa" :style="pupilStyle(142, 78)"/>
            <circle cx="102" cy="74" r="2.5" fill="#fff" :style="pupilStyle(102, 74)"/>
            <circle cx="146" cy="74" r="2.5" fill="#fff" :style="pupilStyle(146, 74)"/>
          </g>

          <!-- 眨眼遮罩 -->
          <g class="ai-lids" v-if="blinking">
            <line x1="84" y1="78" x2="112" y2="78" stroke="#1e1b4b" stroke-width="3" stroke-linecap="round"/>
            <line x1="128" y1="78" x2="156" y2="78" stroke="#1e1b4b" stroke-width="3" stroke-linecap="round"/>
          </g>

          <!-- 嘴巴 -->
          <path class="ai-mouth" d="M105 105 Q120 115 135 105" stroke="#1e1b4b" stroke-width="3" fill="none" stroke-linecap="round"/>

          <!-- 胸前核心 -->
          <circle cx="120" cy="190" r="18" fill="#1e1b4b"/>
          <circle cx="120" cy="190" r="12" fill="#4ade80" filter="url(#glow)">
            <animate attributeName="r" values="10;13;10" dur="2s" repeatCount="indefinite"/>
          </circle>

          <!-- 手臂 -->
          <path d="M70 160 Q45 190 55 220" stroke="#6366f1" stroke-width="14" fill="none" stroke-linecap="round"/>
          <circle cx="55" cy="225" r="10" fill="#818cf8"/>
          <path d="M170 160 Q195 190 185 220" stroke="#6366f1" stroke-width="14" fill="none" stroke-linecap="round"/>
          <circle cx="185" cy="225" r="10" fill="#818cf8"/>
        </svg>

        <!-- 对话气泡 -->
        <div class="ai-bubble">
          <div class="ai-bubble-text">{{ currentTip }}</div>
          <div class="ai-bubble-typing" v-if="typing">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <div class="ai-features">
        <div class="ai-feature">
          <i class="el-icon-cpu"></i>
          <span>AI 流程引导</span>
        </div>
        <div class="ai-feature">
          <i class="el-icon-chat-dot-round"></i>
          <span>智能问答</span>
        </div>
        <div class="ai-feature">
          <i class="el-icon-mic"></i>
          <span>语音播报</span>
        </div>
      </div>

      <div class="left-footer">
        <span>© 2026 Base Room · AI Assistant Powered</span>
      </div>
    </div>

    <!-- 右侧登录区 -->
    <div class="login-right">
      <div class="login-form-wrapper">
        <div class="form-header">
          <h2 class="form-title">欢迎回来</h2>
          <p class="form-subtitle">小 Base 已就绪，登录后随时为你引导业务流程</p>
        </div>

        <el-form :model="form" :rules="rules" ref="form" @submit.native.prevent="handleLogin" class="login-form">
          <div class="field-group">
            <label class="field-label">用户名</label>
            <el-form-item prop="username">
              <el-input v-model="form.username" placeholder="请输入用户名" prefix-icon="el-icon-user" size="large" />
            </el-form-item>
          </div>

          <div class="field-group">
            <label class="field-label">密码</label>
            <el-form-item prop="password">
              <el-input v-model="form.password" :type="showPwd ? 'text' : 'password'" placeholder="请输入密码" prefix-icon="el-icon-lock" size="large">
                <i slot="suffix" :class="showPwd ? 'el-icon-open' : 'el-icon-turn-off'" @click="showPwd = !showPwd" style="cursor:pointer"></i>
              </el-input>
            </el-form-item>
          </div>

          <div class="security-verify" @click="verifyClicked = true">
            <div class="verify-left">
              <i class="el-icon-circle-check" :class="{ verified: verifyClicked }"></i>
              <span>{{ verifyClicked ? '安全验证已通过' : '点击进行安全验证' }}</span>
            </div>
            <i class="el-icon-arrow-right verify-arrow" :class="{ verified: verifyClicked }"></i>
          </div>

          <div class="form-options">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          </div>

          <el-button type="primary" native-type="submit" :loading="loading" class="login-btn">
            登录 <i class="el-icon-arrow-right" v-if="!loading"></i>
          </el-button>
        </el-form>
      </div>

      <div class="right-footer">
        <span>Base Room AI v2.0</span>
      </div>
    </div>
  </div>
</template>

<script>
const TIPS = [
  '你好，我是小 Base，你的 AI 流程助手 👋',
  '登录后我可以帮你引导车牌识别、CRM、ERP、OA 等流程',
  '有任何操作问题，右下角点击我的头像即可对话',
  '我会说话哦，打开语音播报体验更佳',
  '试试问我：「怎么做图片车牌检测？」'
]

export default {
  data() {
    return {
      loading: false,
      showPwd: false,
      verifyClicked: false,
      rememberMe: true,
      mouseX: 0,
      mouseY: 0,
      blinking: false,
      currentTip: TIPS[0],
      typing: false,
      tipIndex: 0,
      form: { username: 'admin', password: '123456' },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },
  mounted() {
    this.startBlink()
    this.startTipLoop()
  },
  beforeDestroy() {
    this.clearTimers()
  },
  methods: {
    onMouseMove(e) {
      this.mouseX = e.clientX
      this.mouseY = e.clientY
    },
    pupilStyle(cx, cy) {
      const rect = this.$refs.aiHuman ? this.$refs.aiHuman.getBoundingClientRect() : { left: 0, top: 0, width: 240, height: 300 }
      const centerX = rect.left + rect.width / 2
      const centerY = rect.top + 78 * (rect.height / 300)
      const dx = this.mouseX - centerX
      const dy = this.mouseY - centerY
      const angle = Math.atan2(dy, dx)
      const dist = Math.min(4, Math.hypot(dx, dy) / 40)
      const x = Math.cos(angle) * dist
      const y = Math.sin(angle) * dist
      return { transform: `translate(${x}px, ${y}px)` }
    },
    particleStyle(n) {
      const size = Math.random() * 3 + 1
      const left = Math.random() * 100
      const delay = Math.random() * 5
      const duration = Math.random() * 10 + 8
      return {
        width: size + 'px',
        height: size + 'px',
        left: left + '%',
        animationDelay: delay + 's',
        animationDuration: duration + 's'
      }
    },
    startBlink() {
      const blink = () => {
        this.blinking = true
        setTimeout(() => { this.blinking = false }, 150)
        this.blinkTimer = setTimeout(blink, Math.random() * 3000 + 2500)
      }
      this.blinkTimer = setTimeout(blink, 3000)
    },
    startTipLoop() {
      this.tipTimer = setInterval(() => {
        this.tipIndex = (this.tipIndex + 1) % TIPS.length
        this.typing = true
        setTimeout(() => {
          this.currentTip = TIPS[this.tipIndex]
          this.typing = false
        }, 600)
      }, 5000)
    },
    clearTimers() {
      clearTimeout(this.blinkTimer)
      clearInterval(this.tipTimer)
    },
    handleLogin() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        this.loading = true
        this.$store.dispatch('user/login', this.form).then(() => {
          this.$router.push('/')
        }).finally(() => this.loading = false)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  height: 100vh;
  display: flex;
  position: relative;
  overflow: hidden;
  background: #0f172a;
}

/* ===== 科技背景 ===== */
.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(99, 102, 241, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99, 102, 241, 0.06) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none;
}

.bg-glow {
  position: absolute;
  top: -20%;
  left: -10%;
  width: 60%;
  height: 80%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.18) 0%, transparent 60%);
  pointer-events: none;
}

.bg-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  span {
    position: absolute;
    bottom: -10px;
    background: rgba(99, 102, 241, 0.5);
    border-radius: 50%;
    animation: float-up linear infinite;
  }
}

@keyframes float-up {
  0% { transform: translateY(0) scale(1); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-110vh) scale(0.5); opacity: 0; }
}

/* ===== 左侧 AI 展示区 ===== */
.login-left {
  flex: 0 0 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 50px;
  position: relative;
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -30%;
    right: -20%;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.15), transparent 60%);
  }
}

.brand-area {
  text-align: center;
  margin-bottom: 30px;
  position: relative;
  z-index: 1;
}

.logo {
  margin-bottom: 16px;
  svg { filter: drop-shadow(0 4px 16px rgba(99, 102, 241, 0.5)); }
}

.brand-title {
  font-size: 34px;
  font-weight: 800;
  color: #fff;
  margin: 0 0 8px 0;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #fff, #c7d2fe);
  -webkit-background-clip: text;
  color: transparent;
}

.brand-sub {
  font-size: 15px;
  color: rgba(199, 210, 254, 0.8);
  margin: 0;
}

/* ===== AI 数字人 ===== */
.ai-human {
  position: relative;
  width: 280px;
  height: 340px;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  z-index: 1;
}

.ai-halo {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -55%);
  width: 260px;
  height: 260px;
  border-radius: 50%;
  border: 2px solid rgba(99, 102, 241, 0.2);
  animation: halo-pulse 3s ease-out infinite;
  &.delay { animation-delay: 1.5s; }
}

@keyframes halo-pulse {
  0% { transform: translate(-50%, -55%) scale(0.9); opacity: 0.6; }
  100% { transform: translate(-50%, -55%) scale(1.3); opacity: 0; }
}

.ai-body {
  animation: ai-float 4s ease-in-out infinite;
  filter: drop-shadow(0 20px 40px rgba(79, 70, 229, 0.35));
}

@keyframes ai-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}

.ai-eyes .pupil {
  transition: transform 0.1s ease-out;
}

.ai-mouth {
  animation: mouth-smile 3s ease-in-out infinite;
}

@keyframes mouth-smile {
  0%, 100% { d: path('M105 105 Q120 115 135 105'); }
  50% { d: path('M105 106 Q120 118 135 106'); }
}

/* 对话气泡 */
.ai-bubble {
  position: absolute;
  top: 20px;
  right: -40px;
  min-width: 180px;
  max-width: 260px;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 18px 18px 4px 18px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  color: #1e1b4b;
  font-size: 13px;
  line-height: 1.6;
  z-index: 2;
  animation: bubble-pop 0.4s ease-out;
}

@keyframes bubble-pop {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.ai-bubble-typing {
  display: flex;
  gap: 4px;
  padding-top: 8px;
  span {
    width: 6px;
    height: 6px;
    background: #6366f1;
    border-radius: 50%;
    animation: typing-dot 1s infinite;
    &:nth-child(2) { animation-delay: 0.2s; }
    &:nth-child(3) { animation-delay: 0.4s; }
  }
}

@keyframes typing-dot {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.ai-features {
  display: flex;
  gap: 20px;
  margin-top: 40px;
  position: relative;
  z-index: 1;
}

.ai-feature {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  color: #c7d2fe;
  font-size: 13px;
  backdrop-filter: blur(8px);
  transition: all 0.3s;
  i { font-size: 15px; color: #4ade80; }
  &:hover {
    background: rgba(255, 255, 255, 0.14);
    transform: translateY(-2px);
  }
}

.left-footer {
  position: absolute;
  bottom: 24px;
  left: 0;
  right: 0;
  text-align: center;
  color: rgba(199, 210, 254, 0.5);
  font-size: 12px;
}

/* ===== 右侧登录区 ===== */
.login-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 60px;
  background: #fff;
  position: relative;
  z-index: 1;
}

.login-form-wrapper {
  width: 100%;
  max-width: 420px;
}

.form-header {
  margin-bottom: 40px;
}

.form-title {
  font-size: 32px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 10px 0;
}

.form-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.field-group {
  margin-bottom: 22px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  margin-bottom: 8px;
}

::v-deep .el-input__inner {
  height: 48px;
  line-height: 48px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s;
  &:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
  }
}

.security-verify {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: #f8fafc;
  border-radius: 10px;
  margin-bottom: 20px;
  cursor: pointer;
  border: 1px solid #e2e8f0;
  transition: all 0.3s;
  &:hover { border-color: #6366f1; background: #f1f5f9; }
}

.verify-left {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #475569;
  font-size: 14px;
  i {
    font-size: 18px;
    color: #94a3b8;
    transition: color 0.3s;
    &.verified { color: #22c55e; }
  }
}

.verify-arrow {
  color: #94a3b8;
  transition: all 0.3s;
  &.verified { color: #22c55e; transform: translateX(3px); }
}

.form-options {
  margin-bottom: 24px;
  ::v-deep .el-checkbox__label { color: #64748b; }
}

.login-btn {
  width: 100%;
  height: 50px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  border: none;
  box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
  transition: all 0.3s;
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(79, 70, 229, 0.4);
  }
}

.right-footer {
  position: absolute;
  bottom: 24px;
  color: #94a3b8;
  font-size: 12px;
}

/* 响应式 */
@media (max-width: 992px) {
  .login-left { display: none; }
  .login-right { flex: 0 0 100%; }
}
</style>
