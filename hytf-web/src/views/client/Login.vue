<template>
  <div class="login-wrap">
    <div class="deco deco-1"></div>
    <div class="deco deco-2"></div>
    <div class="deco deco-3"></div>
    <div class="login-box">
      <div class="brand">恒耀引擎 | 恒耀投放</div>
      <div class="slogan">短视频投放 · 一站式增长平台</div>
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
  height: 100vh; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #ff5f8f 0%, #ff2e63 45%, #ff7eb3 100%);
}
.deco {
  position: absolute; border-radius: 50%; filter: blur(6px);
  background: rgba(255,255,255,.18);
}
.deco-1 { width: 320px; height: 320px; top: -90px; left: -70px; }
.deco-2 { width: 220px; height: 220px; bottom: -60px; right: -40px; background: rgba(255,255,255,.14); }
.deco-3 { width: 120px; height: 120px; top: 40%; right: 14%; background: rgba(255,255,255,.12); }
.login-box {
  position: relative; z-index: 2;
  width: 400px; padding: 44px 36px; background: #fff;
  border-radius: 18px; box-shadow: 0 18px 50px rgba(199, 21, 71, .28);
}
.brand {
  text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 6px;
  background: linear-gradient(135deg, #ff2e63, #ff6b9d);
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.slogan { text-align: center; font-size: 13px; color: #909399; margin-bottom: 26px; }
.tips { text-align: center; margin-top: 12px; font-size: 12px; }
::v-deep .el-button--primary {
  background: linear-gradient(135deg, #2b6cff, #4a90ff); border: none; font-weight: bold;
  box-shadow: 0 6px 16px rgba(43,108,255,.3);
}
</style>