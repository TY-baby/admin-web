<template>
  <el-container class="layout-wrap">
    <!-- ===== 侧边栏 ===== -->
    <el-aside :width="isCollapse ? '64px' : '230px'" class="sidebar">
      <div class="logo-area">
        <div class="logo-icon">
          <svg viewBox="0 0 32 32" width="26" height="26">
            <circle cx="12" cy="16" r="8" fill="#22d3ee" opacity="0.9"/>
            <circle cx="20" cy="16" r="8" fill="#818cf8" opacity="0.9"/>
          </svg>
        </div>
        <transition name="fade">
          <span v-show="!isCollapse" class="logo-text">推流管理后台</span>
        </transition>
      </div>

      <el-menu
        :default-active="$route.path"
        router
        :collapse="isCollapse"
        background-color="transparent"
        text-color="#8896ab"
        active-text-color="#fff"
        class="sidebar-menu">
        <sidebar-item v-for="route in routes" :key="route.path" :item="route" :base-path="route.path" />
      </el-menu>

      <div class="sidebar-footer" v-show="!isCollapse">
        <span class="version">v1.0.0</span>
      </div>
    </el-aside>

    <!-- ===== 主区域 ===== -->
    <el-container class="main-container">
      <el-header class="header" height="56px">
        <div class="header-left">
          <span class="collapse-btn" @click="isCollapse = !isCollapse">
            <i :class="isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'"></i>
          </span>
          <div class="breadcrumb">
            <span class="bc-page">{{ $route.meta.title || '交易信息' }}</span>
          </div>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-info">
              <div class="user-avatar">{{ avatarText }}</div>
              <span class="user-name">{{ userInfo.real_name || userInfo.username || '管理员' }}</span>
              <i class="el-icon-arrow-down"></i>
            </div>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="logout" icon="el-icon-switch-button">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main-content">
        <div class="page-wrapper">
          <router-view />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import SidebarItem from './SidebarItem.vue'

export default {
  name: 'LayoutIndex',
  components: { SidebarItem },
  data() {
    return {
      routes: [],
      userInfo: {},
      isCollapse: false
    }
  },
  computed: {
    avatarText() {
      const name = this.userInfo.real_name || this.userInfo.username || 'A'
      return name.charAt(0)
    }
  },
  created() {
    this.routes = this.$router.options.routes.filter(r => r.path !== '/login' && !r.hidden)
    this.userInfo = JSON.parse(localStorage.getItem('my_user') || '{}')
  },
  methods: {
    handleCommand(cmd) {
      if (cmd === 'logout') {
        this.$confirm('确认退出登录?', '提示', { type: 'warning' }).then(() => {
          this.$store.dispatch('user/logout')
          this.$router.push('/login')
        }).catch(() => {})
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.layout-wrap { height: 100vh; overflow: hidden; }

.sidebar {
  background: linear-gradient(180deg, #0b1220 0%, #16233d 100%);
  display: flex; flex-direction: column;
  transition: width 0.3s ease;
  overflow: hidden; position: relative; z-index: 10;
  box-shadow: 2px 0 14px rgba(0,0,0,0.18);

  &::after {
    content: ''; position: absolute; top: 0; right: 0;
    width: 1px; height: 100%;
    background: linear-gradient(180deg, rgba(34,211,238,0.35), rgba(34,211,238,0.04));
  }
}

.logo-area {
  height: 64px; display: flex; align-items: center; justify-content: center;
  gap: 10px; padding: 0 14px;
  border-bottom: 1px solid rgba(255,255,255,0.07); flex-shrink: 0;
}
.logo-icon svg { filter: drop-shadow(0 2px 8px rgba(34,211,238,0.45)); }
.logo-text {
  font-size: 16px; font-weight: 700; white-space: nowrap; letter-spacing: 1px;
  background: linear-gradient(135deg, #7dd3fc, #a5b4fc);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter, .fade-leave-to { opacity: 0; }

.sidebar-menu {
  flex: 1; overflow-y: auto; overflow-x: hidden;
  border-right: none !important; padding: 10px 8px;

  ::v-deep .el-menu { background-color: transparent !important; border-right: none; }

  ::v-deep .el-menu-item,
  ::v-deep .el-submenu__title {
    height: 44px; line-height: 44px; margin: 3px 0;
    border-radius: 8px; transition: all 0.25s ease; font-size: 14px;

    i { color: #64748b; margin-right: 8px; font-size: 16px; transition: color 0.25s; }
    &:hover { background: rgba(34,211,238,0.10) !important; i { color: #22d3ee; } }
  }

  ::v-deep .el-menu-item.is-active {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: #fff !important;
    box-shadow: 0 4px 14px rgba(14,165,233,0.38);
    i { color: #fff !important; }
  }

  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 2px; }
}

.sidebar-footer {
  padding: 12px 20px; border-top: 1px solid rgba(255,255,255,0.07); flex-shrink: 0;
  .version { font-size: 11px; color: #475569; }
}

.main-container { display: flex; flex-direction: column; overflow: hidden; }

.header {
  background: #fff; display: flex; align-items: center; justify-content: space-between;
  padding: 0 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); position: relative; z-index: 5;
}
.header-left { display: flex; align-items: center; gap: 16px; }
.collapse-btn {
  width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;
  border-radius: 8px; cursor: pointer; color: #64748b; font-size: 18px; transition: all 0.25s;
  &:hover { background: #f1f5f9; color: #0ea5e9; }
}
.bc-page { font-size: 15px; font-weight: 600; color: #1e293b; }
.header-right { display: flex; align-items: center; gap: 8px; }
.user-info {
  display: flex; align-items: center; gap: 8px;
  padding: 4px 12px 4px 4px; border-radius: 24px; cursor: pointer; transition: all 0.25s;
  &:hover { background: #f1f5f9; }
}
.user-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: linear-gradient(135deg, #0ea5e9, #6366f1);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 14px; font-weight: 700;
}
.user-name { font-size: 13px; color: #475569; font-weight: 500; }

.main-content { background: #f0f2f7; overflow-y: auto; padding: 0 !important; }
.page-wrapper { min-height: 100%; padding: 20px; }
</style>