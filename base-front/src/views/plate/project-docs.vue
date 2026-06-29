<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">项目文档</div>
      <div class="hero-desc">后端 Swagger 文档入口与本地说明摘要，便于联调、测试与交接。</div>
    </div>

    <div class="plate-grid-2">
      <div class="plate-card">
        <div class="doc-title">车牌识别后端服务</div>
        <div class="plate-kv">
          <span class="kv-label">系统名称</span>
          <span class="kv-value">{{ docs.system_name || '车牌检测识别平台' }}</span>
          <span class="kv-label">服务地址</span>
          <span class="kv-value">{{ docs.base_url || 'http://127.0.0.1:9999' }}</span>
          <span class="kv-label">接口能力</span>
          <span class="kv-value">{{ docs.abilities || '图片检测、视频检测、资源管理、系统监控、模型管理、LLM、多模态问答' }}</span>
        </div>
        <div class="doc-actions">
          <el-button type="primary" icon="el-icon-link" @click="openSwagger">打开 Swagger</el-button>
          <el-button icon="el-icon-document" @click="summaryVisible=true">本地说明摘要</el-button>
        </div>
      </div>
      <div class="plate-card">
        <div class="doc-title">接口概览</div>
        <el-timeline>
          <el-timeline-item v-for="(item, i) in overview" :key="i" :type="item.type">
            {{ item.title }}
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>

    <el-dialog :visible.sync="summaryVisible" title="本地说明摘要" width="700px">
      <div class="summary-content">
        <p>1. 图片支持 png/jpg/jpeg/gif/bmp，单文件不超过 10MB。</p>
        <p>2. 视频支持 mp4/avi/mov/wmv/flv/mkv，单文件不超过 500MB。</p>
        <p>3. 检测结果视频建议后端输出 H.264 编码以保证浏览器兼容播放。</p>
        <p>4. 识别明细依赖前端本地缓存，清空缓存后需重新检测。</p>
        <p>5. 系统日志当天文件标记为“使用中”，不可删除。</p>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getProjectDocs } from '@/api/modules/plate'
import { handleReq } from './helpers'

export default {
  data() {
    return {
      docs: {},
      summaryVisible: false,
      overview: [
        { title: '图片 / 视频上传与检测', type: 'primary' },
        { title: '图片 / 视频资源管理', type: 'success' },
        { title: '数据可视化与系统监控', type: 'warning' },
        { title: '系统日志与项目文档', type: 'info' },
        { title: '模型管理与 LLM 问答', type: 'danger' }
      ]
    }
  },
  async created() {
    try {
      this.docs = await handleReq(getProjectDocs())
    } catch (e) {
      console.warn('文档加载失败', e)
    }
  },
  methods: {
    openSwagger() {
      const base = this.docs.base_url || 'http://127.0.0.1:9999'
      window.open(base + '/docs', '_blank')
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
.doc-title {
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1e293b;
}
.doc-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}
.summary-content {
  font-size: 14px;
  color: #475569;
  line-height: 2;
}
</style>
