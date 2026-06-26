<template>
  <div class="screen-page" ref="screenRef">
    <header class="screen-header">
      <div class="header-left">
        <span class="back-btn" @click="$router.push('/dashboard')">
          <i class="el-icon-arrow-left"></i> 返回
        </span>
        <span class="header-title">{{ title }}</span>
      </div>
      <div class="header-center">
        <slot name="center" />
      </div>
      <div class="header-right">
        <span class="screen-time">{{ currentTime }}</span>
        <span class="fullscreen-btn" @click="toggleFull">
          <i class="el-icon-full-screen"></i>
        </span>
      </div>
    </header>
    <main class="screen-body">
      <slot />
    </main>
  </div>
</template>

<script>
export default {
  props: {
    title: { type: String, default: '数据大屏' }
  },
  data() {
    return { currentTime: '', timer: null }
  },
  mounted() {
    this.updateTime()
    this.timer = setInterval(this.updateTime, 1000)
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  methods: {
    updateTime() { this.currentTime = new Date().toLocaleString('zh-CN', { hour12: false }) },
    toggleFull() {
      const el = this.$refs.screenRef
      if (!document.fullscreenElement) el.requestFullscreen && el.requestFullscreen()
      else document.exitFullscreen && document.exitFullscreen()
    }
  }
}
</script>

<style lang="scss" scoped>
.screen-page {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: linear-gradient(135deg, #070d24 0%, #0c1432 100%);
  color: #e2e8f0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.screen-header {
  height: 56px;
  min-height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background: linear-gradient(180deg, rgba(8,18,46,0.98), rgba(8,18,46,0.9));
  border-bottom: 1px solid rgba(0,212,255,0.1);
  position: relative;

  &::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 50%;
    transform: translateX(-50%);
    width: 40%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
  }
}

.header-left { display: flex; align-items: center; gap: 16px; }
.back-btn {
  color: #6b8ab5;
  cursor: pointer;
  font-size: 13px;
  transition: color 0.2s;
  &:hover { color: #00d4ff; }
}
.header-title {
  font-size: 18px;
  font-weight: 700;
  background: linear-gradient(90deg, #00d4ff, #a78bfa);
  -webkit-background-clip: text;
  color: transparent;
}
.header-center { position: absolute; left: 50%; transform: translateX(-50%); }
.header-right { display: flex; align-items: center; gap: 16px; color: #6b8ab5; font-size: 13px; }
.fullscreen-btn { cursor: pointer; color: #00d4ff; &:hover { color: #5ce4ff; } }

.screen-body {
  flex: 1;
  padding: 14px 18px;
  overflow: auto;
  min-height: 0;
}
</style>
