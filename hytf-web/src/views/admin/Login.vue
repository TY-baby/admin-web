<template>
  <div class="admin-login">
    <div class="grid"></div>
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
    <div class="glow glow-3"></div>
    <div class="box">
      <div class="brand">恒耀 CRM 管理员</div>
      <div class="sub">HYTF · ADMIN CONSOLE</div>
      <el-form ref="form" :model="form" :rules="rules" label-width="0">
        <el-form-item prop="username">
          <el-input v-model="form.username" prefix-icon="el-icon-user" placeholder="账号" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" prefix-icon="el-icon-lock"
                    placeholder="密码" show-password @keyup.enter.native="onSubmit" />
        </el-form-item>
        <el-button type="primary" class="tech-btn" style="width:100%" :loading="loading" @click="onSubmit">登 录</el-button>
      </el-form>
      <div class="foot">
        默认账号: admin / admin123
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLogin',
  data() {
    return {
      loading: false,
      form: { username: '', password: '' },
      rules: {
        username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },
  methods: {
    onSubmit() {
      this.$refs.form.validate(async ok => {
        if (!ok) return
        this.loading = true
        try {
          await this.$store.dispatch('adminUser/login', this.form)
          this.$message.success('登录成功')
          this.$router.push('/admin/dashboard')
        } catch (e) { /* 拦截器已提示 */ } finally { this.loading = false }
      })
    }
  }
}
</script>

<style scoped lang="scss">
.admin-login {
  position: relative; overflow: hidden;
  height: 100vh; display: flex; align-items: center; justify-content: center;
  background: radial-gradient(circle at 20% 20%, #12325e 0%, #0a1730 45%, #060d1c 100%);
}
// 科技网格背景
.grid {
  position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(0, 220, 255, .07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 220, 255, .07) 1px, transparent 1px);
  background-size: 46px 46px;
  animation: gridmove 18s linear infinite;
}
@keyframes gridmove {
  from { background-position: 0 0, 0 0; }
  to   { background-position: 46px 46px, 46px 46px; }
}
// 发光光球
.glow { position: absolute; border-radius: 50%; filter: blur(70px); opacity: .55; }
.glow-1 { width: 380px; height: 380px; top: -120px; left: -80px; background: #00e5ff; animation: float1 9s ease-in-out infinite; }
.glow-2 { width: 320px; height: 320px; bottom: -100px; right: -60px; background: #6a5cff; animation: float2 11s ease-in-out infinite; }
.glow-3 { width: 220px; height: 220px; top: 45%; right: 20%; background: #00ffa3; opacity: .3; animation: float1 13s ease-in-out infinite; }
@keyframes float1 { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-30px); } }
@keyframes float2 { 0%,100% { transform: translateY(0); } 50% { transform: translateY(26px); } }
// 玻璃拟态卡片
.box {
  position: relative; z-index: 2;
  width: 400px; padding: 44px 36px;
  background: rgba(255, 255, 255, .07);
  backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(0, 229, 255, .28);
  border-radius: 16px;
  box-shadow: 0 0 40px rgba(0, 229, 255, .18), inset 0 0 20px rgba(255,255,255,.04);
}
.brand {
  text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 2px;
  background: linear-gradient(90deg, #00e5ff, #6a5cff);
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.sub { text-align: center; font-size: 11px; letter-spacing: 4px; color: rgba(0,229,255,.5); margin: 6px 0 28px; }
.foot { text-align: center; margin-top: 14px; font-size: 12px; color: rgba(255,255,255,.4); }
// 输入框科技风
::v-deep .el-input__inner {
  background: rgba(255,255,255,.06); border: 1px solid rgba(0,229,255,.25);
  color: #e8f6ff;
  &::placeholder { color: rgba(232,246,255,.35); }
  &:focus { border-color: #00e5ff; box-shadow: 0 0 10px rgba(0,229,255,.3); }
}
::v-deep .el-input__prefix { color: rgba(0,229,255,.6); }
.tech-btn {
  background: linear-gradient(90deg, #00c6ff, #6a5cff) !important; border: none !important;
  font-weight: bold; letter-spacing: 4px; color: #fff !important;
  box-shadow: 0 0 20px rgba(0, 198, 255, .4);
  transition: box-shadow .2s ease, transform .15s ease;
  &:hover { box-shadow: 0 0 30px rgba(0, 198, 255, .65); transform: translateY(-1px); }
}
</style>