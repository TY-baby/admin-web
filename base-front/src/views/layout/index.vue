<template>
  <el-container class="layout-wrap">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '240px'" class="sidebar">
      <div class="logo-area">
        <div class="logo-icon">
          <svg viewBox="0 0 32 32" width="28" height="28">
            <circle cx="12" cy="16" r="8" fill="#60a5fa" opacity="0.9"/>
            <circle cx="20" cy="16" r="8" fill="#818cf8" opacity="0.9"/>
          </svg>
        </div>
        <transition name="fade">
          <span v-show="!isCollapse" class="logo-text">Base Room</span>
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

    <!-- 右侧主区域 -->
    <el-container class="main-container">
      <!-- 顶部导航 -->
      <el-header class="header" height="56px">
        <div class="header-left">
          <span class="collapse-btn" @click="isCollapse = !isCollapse">
            <i :class="isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'"></i>
          </span>
          <div class="breadcrumb">
            <span class="bc-page">{{ $route.meta.title || '工作台' }}</span>
          </div>
        </div>
        <div class="header-right">
          <span class="header-action" @click="$router.push('/bigscreen')">
            <i class="el-icon-data-board"></i>
            <span>大屏</span>
          </span>
          <el-dropdown @command="handleCommand" trigger="click">
            <div class="user-info">
              <div class="user-avatar">
                {{ (userInfo.real_name || userInfo.username || 'A').charAt(0) }}
              </div>
              <span class="user-name">{{ userInfo.real_name || userInfo.username }}</span>
              <i class="el-icon-arrow-down"></i>
            </div>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="logout" icon="el-icon-switch-button">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 页面内容 -->
      <el-main class="main-content">
        <div class="page-wrapper">
          <router-view />
        </div>
      </el-main>
    </el-container>

    <!-- AI 数字人助手 -->
    <digital-human />
  </el-container>
</template>

<script>
import SidebarItem from './SidebarItem.vue'
import DigitalHuman from '@/components/DigitalHuman'
export default {
  components: { SidebarItem, DigitalHuman },
  data() {
    return {
      routes: [],
      userInfo: {},
      isCollapse: false
    }
  },
  created() {
    this.routes = this.$router.options.routes.filter(r => r.path !== '/login' && r.path !== '/bigscreen/fullscreen')
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

<style lang="scss" scoped>
.layout-wrap {
  height: 100vh;
  overflow: hidden;
}

/* ===== 侧边栏 ===== */
.sidebar {
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  overflow: hidden;
  position: relative;
  z-index: 10;
  box-shadow: 2px 0 12px rgba(0,0,0,0.15);

  &::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 1px; height: 100%;
    background: linear-gradient(180deg, rgba(99,102,241,0.3), rgba(99,102,241,0.05));
  }
}

.logo-area {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}

.logo-icon {
  flex-shrink: 0;
  svg { filter: drop-shadow(0 2px 8px rgba(99,102,241,0.4)); }
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(135deg, #60a5fa, #818cf8);
  -webkit-background-clip: text;
  color: transparent;
  white-space: nowrap;
  letter-spacing: 1px;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter, .fade-leave-to { opacity: 0; }

/* 菜单样式 */
.sidebar-menu {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  border-right: none !important;
  padding: 8px;

  ::v-deep .el-menu {
    background-color: transparent !important;
    border-right: none;
  }

  ::v-deep .el-menu-item,
  ::v-deep .el-submenu__title {
    height: 44px;
    line-height: 44px;
    margin: 2px 0;
    border-radius: 8px;
    transition: all 0.25s ease;
    font-size: 14px;

    i {
      color: #64748b;
      margin-right: 8px;
      font-size: 16px;
      transition: color 0.25s;
    }

    &:hover {
      background: rgba(99,102,241,0.08) !important;
      i { color: #818cf8; }
    }
  }

  ::v-deep .el-menu-item.is-active {
    background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
    color: #fff !important;
    box-shadow: 0 4px 12px rgba(99,102,241,0.35);

    i { color: #fff !important; }

    &::before {
      content: '';
      position: absolute;
      left: 0; top: 50%;
      transform: translateY(-50%);
      width: 3px; height: 60%;
      background: #fff;
      border-radius: 0 3px 3px 0;
    }
  }

  ::v-deep .el-submenu.is-opened > .el-submenu__title {
    color: #c8d8ec;
    i { color: #818cf8; }
  }

  ::v-deep .el-submenu .el-menu-item {
    padding-left: 52px !important;
    min-width: auto;
    font-size: 13px;
    height: 40px;
    line-height: 40px;
    color: #8896ab;

    &.is-active {
      background: rgba(99,102,241,0.12) !important;
      color: #a5b4fc !important;
      box-shadow: none;
    }
  }

  ::v-deep .el-submenu__icon-arrow {
    color: #64748b;
  }

  /* 滚动条 */
  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-track { background: transparent; }
  &::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }
}

.sidebar-footer {
  padding: 12px 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;

  .version {
    font-size: 11px;
    color: #475569;
  }
}

/* ===== 主容器 ===== */
.main-container {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ===== 顶部导航 ===== */
.header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  position: relative;
  z-index: 5;

  &::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, #e2e8f0, #f1f5f9, #e2e8f0);
  }
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  width: 36px; height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  cursor: pointer;
  color: #64748b;
  font-size: 18px;
  transition: all 0.25s;

  &:hover {
    background: #f1f5f9;
    color: #4f46e5;
  }
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bc-page {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-action {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 13px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.25s;
  background: #f8fafc;

  &:hover {
    background: #eef2ff;
    color: #4f46e5;
  }

  i { font-size: 15px; }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px 4px 4px;
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.25s;

  &:hover { background: #f1f5f9; }
}

.user-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #818cf8);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
}

.user-name {
  font-size: 13px;
  color: #475569;
  font-weight: 500;
}

/* ===== 页面内容区 ===== */
.main-content {
  background: #f0f2f7;
  overflow-y: auto;
  padding: 0 !important;
}

.page-wrapper {
  min-height: 100%;
  padding: 20px;
}

/* ===== 折叠状态 ===== */
.sidebar .el-menu--collapse {
  ::v-deep .el-submenu__title span,
  ::v-deep .el-submenu__title .el-submenu__icon-arrow {
    display: none;
  }
}
</style>
