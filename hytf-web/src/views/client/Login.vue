<template>
  <div class="login-wrap">
    <div class="login-box">
      <div class="brand">鎭掕€€寮曟搸 | 鎭掕€€鎶曟斁</div>
      <el-form ref="form" :model="form" :rules="rules" label-width="0" @submit.native.prevent="onSubmit">
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="璇疯緭鍏ユ墜鏈哄彿" prefix-icon="el-icon-mobile-phone" maxlength="11" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="璇疯緭鍏ュ瘑鐮? prefix-icon="el-icon-lock" show-password @keyup.enter.native="onSubmit" />
        </el-form-item>
        <el-button type="primary" style="width:100%" :loading="loading" @click="onSubmit">鐧?褰?/el-button>
      </el-form>
      <div class="tips text-muted">榛樿瀵嗙爜瑙勫垯锛氭墜鏈哄彿 + 123</div>
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
          { required: true, message: '璇疯緭鍏ユ墜鏈哄彿', trigger: 'blur' },
          { validator: (r, v, cb) => (isPhone(v) ? cb() : cb(new Error('鎵嬫満鍙锋牸寮忎笉姝ｇ‘'))), trigger: 'blur' }
        ],
        password: [
          { required: true, message: '璇疯緭鍏ュ瘑鐮?, trigger: 'blur' },
          { min: 6, max: 32, message: '闀垮害6-32浣?, trigger: 'blur' }
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
          this.$message.success('鐧诲綍鎴愬姛')
          this.$router.push('/client/home')
        } catch (e) { /* 鎷︽埅鍣ㄥ凡鎻愮ず */ } finally { this.loading = false }
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