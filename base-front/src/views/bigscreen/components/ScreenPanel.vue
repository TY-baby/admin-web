<template>
  <div class="screen-panel" :style="{height: height}">
    <div class="panel-title-bar" v-if="title">
      <span class="title-icon"></span>
      <span class="title-text">{{ title }}</span>
      <span class="title-extra"><slot name="extra" /></span>
    </div>
    <div class="panel-content"><slot /></div>
  </div>
</template>

<script>
export default {
  props: {
    title: { type: String, default: '' },
    height: { type: String, default: 'auto' }
  }
}
</script>

<style lang="scss" scoped>
.screen-panel {
  background: linear-gradient(135deg, rgba(12,26,58,0.85) 0%, rgba(8,18,46,0.95) 100%);
  border: 1px solid rgba(0,212,255,0.12);
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.04);
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  backdrop-filter: blur(8px);

  &::before {
    content: '';
    position: absolute;
    top: 0; left: 20px; right: 20px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.35), transparent);
  }

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 12px;
    pointer-events: none;
    box-shadow: inset 0 0 30px rgba(0,212,255,0.03);
  }
}

.panel-title-bar {
  height: 42px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  border-bottom: 1px solid rgba(0,212,255,0.08);
  flex-shrink: 0;
}

.title-icon {
  width: 4px; height: 14px;
  border-radius: 2px;
  background: linear-gradient(180deg, #00d4ff, #6366f1);
}

.title-text {
  font-size: 14px;
  font-weight: 600;
  color: #e2e8f0;
  letter-spacing: 1px;
}

.title-extra {
  margin-left: auto;
  font-size: 12px;
  color: #6b8ab5;
}

.panel-content {
  flex: 1;
  min-height: 0;
  position: relative;
  padding: 12px;
}
</style>
