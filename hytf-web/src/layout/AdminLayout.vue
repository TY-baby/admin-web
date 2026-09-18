<template>
  <el-container style="height: 100vh">
    <el-aside width="220px" class="tech-aside">
      <div class="aside-logo">恒耀 CRM</div>
      <el-menu :default-active="$route.path" router class="tech-menu"
               background-color="#0b2a5e" text-color="#a8c4f0" active-text-color="#00e5ff">
        <el-menu-item index="/admin/dashboard"><i class="el-icon-s-home"></i><span>首页</span></el-menu-item>
        <el-menu-item index="/admin/customer"><i class="el-icon-user"></i><span>用户管理</span></el-menu-item>
        <el-menu-item index="/admin/invoice"><i class="el-icon-document"></i><span>开票管理</span></el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="flex-between tech-header">
        <div class="page-title">{{ $route.meta.title }}</div>
        <div>
          <span class="text-muted" style="margin-right:12px">{{ info.username || info.real_name || '管理员' }}</span>
          <el-button type="text" @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-main class="tech-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'AdminLayout',
  computed: { ...mapState('adminUser', ['info']) },
  methods: {
    logout() {
      this.$confirm('确定退出登录吗?', '提示', { type: 'warning' }).then(() => {
        this.$store.dispatch('adminUser/logout')
        this.$router.push('/admin/login')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped lang="scss">
// 科技蓝侧边栏
.tech-aside {
  background: linear-gradient(180deg, #0a2a5e 0%, #0b2f6b 60%, #0d3a80 100%);
  box-shadow: 2px 0 12px rgba(10, 42, 94, .3);
}
.aside-logo {
  height: 60px; line-height: 60px; text-align: center;
  font-size: 18px; font-weight: bold; letter-spacing: 2px; color: #fff;
  background: linear-gradient(90deg, rgba(0,229,255,.15), rgba(31,107,255,.15));
  border-bottom: 1px solid rgba(0,229,255,.2);
}
.tech-menu { border-right: none; }
::v-deep .tech-menu .el-menu-item.is-active {
  background: linear-gradient(90deg, rgba(0,229,255,.18), transparent) !important;
  border-right: 3px solid #00e5ff;
}
// 顶栏
.tech-header {
  background: #fff; border-bottom: 2px solid #1f6bff;
  .page-title { font-size: 16px; font-weight: bold; color: #0b2a5e; }
}
// 主区浅蓝底
.tech-main { background: #eef5ff; padding: 16px; }
// 科技蓝主按钮（作用于子页面）
::v-deep .el-button--primary {
  background: linear-gradient(90deg, #1f6bff, #00c2ff); border: none;
  box-shadow: 0 4px 12px rgba(31,107,255,.25);
  &:hover { opacity: .9; }
}
::v-deep .el-button--text { color: #1f6bff; }
</style>