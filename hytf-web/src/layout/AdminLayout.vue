<template>
  <el-container style="height: 100vh">
    <el-aside width="220px" style="background:#001529">
      <div style="height:60px;line-height:60px;color:#fff;text-align:center;font-size:18px;font-weight:bold">恒耀 CRM</div>
      <el-menu :default-active="$route.path" router background-color="#001529" text-color="#c0c4cc" active-text-color="#fff">
        <el-menu-item index="/admin/dashboard"><i class="el-icon-s-home"></i><span>首页</span></el-menu-item>
        <el-menu-item index="/admin/customer"><i class="el-icon-user"></i><span>用户管理</span></el-menu-item>
        <el-menu-item index="/admin/invoice"><i class="el-icon-document"></i><span>开票管理</span></el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="flex-between" style="background:#fff;border-bottom:1px solid #eee">
        <div style="font-size:16px;font-weight:bold">{{ $route.meta.title }}</div>
        <div>
          <span class="text-muted" style="margin-right:12px">{{ info.username || info.real_name || '管理员' }}</span>
          <el-button type="text" @click="logout">退出</el-button>
        </div>
      </el-header>
      <el-main style="background:#f5f7fa;padding:16px">
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