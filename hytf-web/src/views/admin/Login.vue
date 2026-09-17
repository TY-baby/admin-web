<template>
  <div class="admin-login">
    <div class="box">
      <div class="brand">鎭掕€€ CRM 绠＄悊绔?/div>
      <el-form ref="form" :model="form" :rules="rules" label-width="0">
        <el-form-item prop="username">
          <el-input v-model="form.username" prefix-icon="el-icon-user" placeholder="璐﹀彿" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" prefix-icon="el-icon-lock"
                    placeholder="瀵嗙爜" show-password @keyup.enter.native="onSubmit" />
        </el-form-item>
        <el-button type="primary" style="width:100%" :loading="loading" @click="onSubmit">鐧?褰?/el-button>
      </el-form>
      <div class="text-muted" style="text-align:center;margin-top:12px;font-size:12px">
        榛樿璐﹀彿: admin / admin123
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
        username: [{ required: true, message: '璇疯緭鍏ヨ处鍙?, trigger: 'blur' }],
        password: [{ required: true, message: '璇疯緭鍏ュ瘑鐮?, trigger: 'blur' }]
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
          this.$message.success('鐧诲綍鎴愬姛')
          this.$router.push('/admin/dashboard')
        } catch (e) { /* 鎷︽埅鍣ㄥ凡鎻愮ず */ } finally { this.loading = false }
      })
    }
  }
}
</script>

<style scoped lang="scss">
.admin-login {
  height: 100vh; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #232526 0%, #414345 100%);
}
.box {
  width: 400px; padding: 40px 32px; background: #fff;
  border-radius: 8px; box-shadow: 0 8px 30px rgba(0,0,0,.3);
}
.brand { text-align: center; font-size: 22px; font-weight: bold; margin-bottom: 24px; color: #303133; }
</style>