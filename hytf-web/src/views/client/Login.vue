<template>
  <div class="login-wrap">
    <div class="bg-grid"></div>
    <div class="ring ring-1"></div>
    <div class="ring ring-2"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>

    <div class="hero">
      <div class="hero-logo">恒耀引擎 | 恒耀投放</div>
      <div class="hero-title">电商营销新体验</div>
      <div class="hero-sub">恒耀江海阔 · 风好正扬帆</div>
      <div class="cube">
        <div class="bar b1"></div>
        <div class="bar b2"></div>
        <div class="bar b3"></div>
      </div>
    </div>

    <div class="login-box">
      <div class="brand">登录恒耀引擎账号</div>
      <el-form ref="form" :model="form" :rules="rules" label-width="0" @submit.native.prevent="onSubmit">
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号" prefix-icon="el-icon-mobile-phone" maxlength="11" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" prefix-icon="el-icon-lock" show-password @keyup.enter.native="onSubmit" />
        </el-form-item>
        <el-button type="primary" style="width:100%" :loading="loading" @click="onSubmit">登 录</el-button>
      </el-form>
      <div class="tips text-muted">默认密码规则：手机号 + 123</div>
    </div>
  </div>
</template>

<script>
import { isPhone } from '@/utils/validate'
export default {
  name: 'ClientLogin',
  data() {
    return {
      loading: false,
      form: { phone: '', password: '' },
      rules: {
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { validator: (r, v, cb) => (isPhone(v) ? cb() : cb(new Error('手机号格式不正确'))), trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 32, message: '长度6-32位', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    onSubmit() {
      this.$refs.form.validate(async ok => {
        if (!ok) return
        this.loading = true
        try {
          await this.$store.dispatch('clientUser/login', this.form)
          this.$message.success('登录成功')
          this.$router.push('/client/home')
        } catch (e) { /* 拦截器已提示 */ } finally { this.loading = false }
      })
    }
  }
}
</script>

<style scoped lang="scss">
.login-wrap {
  position: relative; overflow: hidden;
  height: 100vh; display: flex; align-items: center; justify-content: space-between;
  padding: 0 8%;
  background: linear-gradient(135deg, #eaf4ff 0%, #d7e9ff 40%, #f2f8ff 100%);
}
// 细网格科技底纹
.bg-grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(43,108,255,.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(43,108,255,.05) 1px, transparent 1px);
  background-size: 44px 44px;
}
// 同心环（3D 轨道感）
.ring { position: absolute; border-radius: 50%; border: 2px solid rgba(43,140,255,.18); }
.ring-1 { width: 620px; height: 620px; left: -160px; top: 50%; transform: translateY(-50%) rotateX(60deg); border-color: rgba(0,180,255,.25); }
.ring-2 { width: 460px; height: 460px; left: -80px; top: 50%; transform: translateY(-50%) rotateX(60deg); border-color: rgba(43,108,255,.2); }
// 发光光球
.orb { position: absolute; border-radius: 50%; filter: blur(50px); opacity: .5; }
.orb-1 { width: 300px; height: 300px; top: -80px; right: 10%; background: #7cc4ff; }
.orb-2 { width: 240px; height: 240px; bottom: -60px; left: 30%; background: #9fd8ff; }
.orb-3 { width: 160px; height: 160px; top: 30%; left: 46%; background: #bfe6ff; opacity: .6; }

// 左侧品牌区
.hero { position: relative; z-index: 2; color: #123c8c; max-width: 46%; }
.hero-logo { font-size: 20px; font-weight: bold; color: #1f6bff; letter-spacing: 1px; }
.hero-title { font-size: 44px; font-weight: 800; margin-top: 28px; letter-spacing: 2px;
  background: linear-gradient(90deg, #1f6bff, #00c2ff);
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { font-size: 18px; letter-spacing: 6px; color: #3a6fd8; margin-top: 10px; }
.cube { display: flex; align-items: flex-end; gap: 14px; height: 120px; margin-top: 40px; }
.bar { width: 46px; border-radius: 8px 8px 0 0;
  background: linear-gradient(180deg, #00c2ff, #1f6bff);
  box-shadow: 0 8px 24px rgba(31,107,255,.35); }
.b1 { height: 56px; } .b2 { height: 88px; } .b3 { height: 120px; }

// 右侧登录卡
.login-box {
  position: relative; z-index: 2;
  width: 400px; padding: 40px 34px; background: rgba(255,255,255,.92);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
  border-radius: 16px; border: 1px solid rgba(43,108,255,.15);
  box-shadow: 0 18px 50px rgba(31, 107, 255, .18);
}
.brand { text-align: center; font-size: 20px; font-weight: bold; color: #123c8c; margin-bottom: 24px; }
.tips { text-align: center; margin-top: 12px; font-size: 12px; }
::v-deep .el-button--primary {
  background: linear-gradient(90deg, #1f6bff, #00c2ff); border: none; font-weight: bold;
  box-shadow: 0 6px 16px rgba(31,107,255,.3);
}
::v-deep .el-input__inner { background: #f2f7ff; border-color: #d8e6ff;
  &:focus { border-color: #1f6bff; background: #fff; } }

@media (max-width: 900px) {
  .login-wrap { justify-content: center; }
  .hero { display: none; }
}
</style>
