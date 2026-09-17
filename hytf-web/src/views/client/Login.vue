<template>
  <div class="login-wrap">
    <div class="login-box">
      <div class="brand">恒耀引擎 | 恒耀投放</div>
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
  height: 100vh; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
}
.login-box {
  width: 400px; padding: 40px 32px; background: #fff;
  border-radius: 8px; box-shadow: 0 8px 30px rgba(0,0,0,.2);
}
.brand { text-align: center; font-size: 22px; font-weight: bold; color: #303133; margin-bottom: 24px; }
.tips { text-align: center; margin-top: 12px; font-size: 12px; }
</style>