<template>
  <el-container class='layout-wrap'>
    <el-aside width='220px' class='sidebar'>
      <div class='logo'>Base Room CRM</div>
      <el-menu :default-active='$route.path' router background-color='#001529' text-color='#fff' active-text-color='#409EFF'>
        <sidebar-item v-for='route in routes' :key='route.path' :item='route' :base-path='route.path' />
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class='header'>
        <span>{{ $route.meta.title || '工作台' }}</span>
        <div class='header-right'>
          <el-button type='text' icon='el-icon-full-screen' @click='$router.push("/bigscreen")'>智慧大屏</el-button>
          <el-dropdown @command='handleCommand'>
            <span class='el-dropdown-link'>{{ userInfo.real_name || userInfo.username }}<i class='el-icon-arrow-down el-icon--right'></i></span>
            <el-dropdown-menu slot='dropdown'>
              <el-dropdown-item command='logout'>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class='main'>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import SidebarItem from './SidebarItem.vue'
export default {
  components: { SidebarItem },
  data() {
    return {
      routes: [],
      userInfo: {}
    }
  },
  created() {
    this.routes = this.$router.options.routes.filter(r => r.path !== '/login' && r.path !== '/bigscreen')
    this.userInfo = JSON.parse(localStorage.getItem('base_user') || '{}')
  },
  methods: {
    handleCommand(cmd) {
      if (cmd === 'logout') {
        localStorage.clear()
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>
.layout-wrap { height: 100vh; }
.sidebar { background: #001529; color: #fff; }
.logo { height: 60px; line-height: 60px; text-align: center; font-size: 18px; font-weight: bold; border-bottom: 1px solid rgba(255,255,255,0.1); }
.header { background: #fff; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
.header-right { display: flex; align-items: center; gap: 20px; }
.main { background: #f5f7fa; }
</style>
