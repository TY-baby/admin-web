<template>
  <div class="login-page">
    <!-- 左侧宣传区 -->
    <div class="login-left">
      <div class="brand-area">
        <div class="logo">
          <svg viewBox="0 0 48 48" width="48" height="48">
            <circle cx="18" cy="24" r="12" fill="#4ADE80" opacity="0.85"/>
            <circle cx="30" cy="24" r="12" fill="#60A5FA" opacity="0.85"/>
          </svg>
        </div>
        <h1 class="brand-title">Base Room CRM</h1>
        <p class="brand-sub">企业级客户关系管理平台</p>
      </div>
      <div class="features">
        <div class="feature-item">
          <div class="feature-icon">
            <i class="el-icon-s-check"></i>
          </div>
          <div class="feature-text">
            <div class="feature-name">安全可靠</div>
            <div class="feature-desc">多重数据加密，保障企业信息安全</div>
          </div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">
            <i class="el-icon-lightning"></i>
          </div>
          <div class="feature-text">
            <div class="feature-name">高效便捷</div>
            <div class="feature-desc">智能工作流，提升团队协作效率</div>
          </div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">
            <i class="el-icon-s-grid"></i>
          </div>
          <div class="feature-text">
            <div class="feature-name">功能强大</div>
            <div class="feature-desc">客户、商机、订单全链路管理</div>
          </div>
        </div>
      </div>
      <div class="left-footer">
        <span>© 2026 Base Room</span>
      </div>
    </div>

    <!-- 右侧登录区 -->
    <div class="login-right">
      <div class="login-form-wrapper">
        <h2 class="form-title">欢迎回来</h2>
        <p class="form-subtitle">请登录您的账户</p>

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
                <i slot="suffix" :class="showPwd ? 'el-icon-view' : 'el-icon-view'" @click="showPwd = !showPwd" style="cursor:pointer"></i>
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
        <span>Base Room CRM v1.0</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      showPwd: false,
      verifyClicked: false,
      rememberMe: true,
      form: { username: 'admin', password: '123456' },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },
  methods: {
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
  background: #f5f7fa;
}

/* ===== 左侧宣传区 ===== */
.login-left {
  flex: 0 0 45%;
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 60px 50px;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -30%;
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: rgba(255,255,255,0.03);
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -20%;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: rgba(255,255,255,0.03);
  }
}

.brand-area {
  text-align: center;
  margin-bottom: 60px;
  position: relative;
  z-index: 1;
}

.logo {
  margin-bottom: 20px;
  svg {
    filter: drop-shadow(0 4px 12px rgba(0,0,0,0.2));
  }
}

.brand-title {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px 0;
  letter-spacing: 1px;
}

.brand-sub {
  font-size: 15px;
  color: rgba(255,255,255,0.7);
  margin: 0;
}

.features {
  width: 100%;
  max-width: 360px;
  position: relative;
  z-index: 1;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 28px;
  padding: 16px 20px;
  border-radius: 12px;
  background: rgba(255,255,255,0.08);
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;

  &:hover {
    background: rgba(255,255,255,0.14);
    transform: translateX(4px);
  }

  &:last-child { margin-bottom: 0; }
}

.feature-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(255,255,255,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 20px;
  color: #93c5fd;
}

.feature-text { flex: 1; }

.feature-name {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 4px;
}

.feature-desc {
  font-size: 12px;
  color: rgba(255,255,255,0.6);
  line-height: 1.5;
}

.left-footer {
  position: absolute;
  bottom: 30px;
  color: rgba(255,255,255,0.4);
  font-size: 12px;
}

/* ===== 右侧登录区 ===== */
.login-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #fff;
  padding: 40px;
  position: relative;
}

.login-form-wrapper {
  width: 100%;
  max-width: 420px;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 6px 0;
}

.form-subtitle {
  font-size: 14px;
  color: #94a3b8;
  margin: 0 0 36px 0;
}

.login-form {
  ::v-deep .el-form-item {
    margin-bottom: 0;
  }

  ::v-deep .el-input__inner {
    height: 46px;
    line-height: 46px;
    border-radius: 10px;
    border: 1.5px solid #e2e8f0;
    font-size: 14px;
    transition: all 0.3s;

    &:focus {
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
    }
  }

  ::v-deep .el-input__prefix {
    left: 12px;
    font-size: 16px;
    color: #94a3b8;
  }

  ::v-deep .el-input--prefix .el-input__inner {
    padding-left: 40px;
  }
}

.field-group {
  margin-bottom: 22px;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
}

/* 安全验证 */
.security-verify {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  border-radius: 10px;
  border: 1.5px solid #e2e8f0;
  background: #f8fafc;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.3s ease;

  &:hover {
    border-color: #3b82f6;
    background: #eff6ff;
  }

  .verify-left {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    color: #64748b;

    i { font-size: 18px; color: #94a3b8; }
    i.verified { color: #22c55e; }
  }

  .verify-arrow {
    font-size: 14px;
    color: #94a3b8;
    transition: all 0.3s;
  }

  .verify-arrow.verified {
    color: #22c55e;
  }
}

.form-options {
  margin-bottom: 28px;

  ::v-deep .el-checkbox__label {
    font-size: 13px;
    color: #64748b;
  }
}

.login-btn {
  width: 100%;
  height: 48px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  border: none;
  letter-spacing: 2px;
  transition: all 0.3s ease;

  &:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    transform: translateY(-1px);
    box-shadow: 0 8px 25px rgba(37,99,235,0.35);
  }

  &:active {
    transform: translateY(0);
  }
}

.right-footer {
  position: absolute;
  bottom: 24px;
  right: 30px;
  font-size: 12px;
  color: #cbd5e1;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
  .login-left {
    display: none;
  }
  .login-right {
    padding: 30px 20px;
  }
}
</style>
