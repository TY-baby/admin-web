<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">图片车牌检测识别</div>
      <div class="hero-desc">支持单张与批量图片上传，自动完成车牌定位、字符识别与结果可视化展示。</div>
    </div>

    <div class="plate-stat-row">
      <div class="plate-stat-card" v-for="(s, i) in stats" :key="i">
        <div class="stat-label">{{ s.label }}</div>
        <div class="stat-value">{{ s.value }}</div>
      </div>
    </div>

    <div class="plate-card">
      <div class="plate-toolbar">
        <div class="plate-actions">
          <el-upload action="" :http-request="handleUpload" :show-file-list="false" accept="image/*" multiple>
            <el-button type="primary" icon="el-icon-upload2">上传图片</el-button>
          </el-upload>
          <el-button type="success" icon="el-icon-cpu" :disabled="!selected.length" @click="batchDetect">批量检测</el-button>
          <el-button icon="el-icon-refresh" @click="load">刷新列表</el-button>
        </div>
      </div>

      <el-table :data="list" v-loading="loading" border @selection-change="onSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="filename" label="文件名" />
        <el-table-column label="缩略图" width="120">
          <template slot-scope="scope">
            <img :src="scope.row.url" class="thumb" @click="preview(scope.row)" />
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'detected' ? 'success' : 'info'">
              {{ scope.row.status === 'detected' ? '已检测' : '未检测' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="上传时间" width="180">
          <template slot-scope="scope">{{ formatDate(scope.row.create_time) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template slot-scope="scope">
            <el-button type="text" @click="detect(scope.row)">检测</el-button>
            <el-button type="text" :disabled="scope.row.status !== 'detected'" @click="showResult(scope.row)">结果</el-button>
            <el-button type="text" style="color:#f56c6c" @click="remove(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog :visible.sync="compareVisible" title="原图与结果对比" width="900px">
      <div class="plate-preview-grid" v-if="current">
        <div class="preview-panel">
          <div class="preview-label">原始图片</div>
          <img :src="current.url" class="preview-media" />
        </div>
        <div class="preview-panel">
          <div class="preview-label">检测结果</div>
          <img :src="current.result_url || current.url" class="preview-media" />
        </div>
      </div>
    </el-dialog>

    <el-drawer :visible.sync="detailVisible" title="识别明细" size="420px">
      <div v-if="detail" class="detail-wrap">
        <div class="plate-kv">
          <span class="kv-label">识别摘要</span>
          <span class="kv-value">{{ detectionSummary(detail) }}</span>
        </div>
        <el-divider />
        <div v-for="(p, i) in detail.plates" :key="i" class="plate-item">
          <div class="plate-title">车牌 {{ i + 1 }}</div>
          <div class="plate-kv">
            <span class="kv-label">车牌号</span><span class="kv-value">{{ p.plate_no }}</span>
            <span class="kv-label">车牌颜色</span><span class="kv-value">{{ plateColorLabel(p.plate_color) }}</span>
            <span class="kv-label">单双层</span><span class="kv-value">{{ plateTypeLabel(p.plate_type) }}</span>
            <span class="kv-label">检测置信度</span><span class="kv-value">{{ formatPercent(p.confidence) }}</span>
            <span class="kv-label">颜色置信度</span><span class="kv-value">{{ formatPercent(p.color_conf) }}</span>
            <span class="kv-label">检测框</span><span class="kv-value">{{ p.box }}</span>
            <span class="kv-label">角点</span><span class="kv-value">{{ p.landmarks }}</span>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import {
  getImageList, uploadImage, detectImage, batchDetectImage, deleteImage, getImageDetail
} from '@/api/modules/plate'
import {
  formatDate, formatPercent, plateTypeLabel, plateColorLabel, detectionSummary,
  getImageCache, setImageCache, handleReq, staticImageUrl
} from './helpers'

export default {
  data() {
    return {
      loading: false,
      list: [],
      selected: [],
      stats: [
        { label: '原始图片数', value: 0 },
        { label: '检测结果图数', value: 0 },
        { label: '缓存明细数', value: 0 },
        { label: '已勾选图片数', value: 0 }
      ],
      compareVisible: false,
      detailVisible: false,
      current: null,
      detail: null
    }
  },
  created() { this.load() },
  methods: {
    formatDate, formatPercent, plateTypeLabel, plateColorLabel, detectionSummary,
    async load() {
      this.loading = true
      try {
        const data = await handleReq(getImageList())
        this.list = (data || []).map(item => ({ ...item, url: staticImageUrl(item.path) }))
        const cache = getImageCache()
        this.stats[0].value = this.list.length
        this.stats[1].value = this.list.filter(i => i.status === 'detected').length
        this.stats[2].value = Object.keys(cache).length
        this.stats[3].value = this.selected.length
      } finally {
        this.loading = false
      }
    },
    onSelectionChange(rows) {
      this.selected = rows
      this.stats[3].value = rows.length
    },
    async handleUpload({ file }) {
      const fd = new FormData()
      fd.append('file', file)
      await handleReq(uploadImage(fd))
      this.$message.success('上传成功')
      this.load()
    },
    async detect(row) {
      const res = await handleReq(detectImage({ id: row.id }))
      this.$message.success('检测完成')
      row.status = 'detected'
      row.result_path = res.result_path
      row.result_url = staticImageUrl(res.result_path)
      const cache = getImageCache()
      cache[row.id] = res
      setImageCache(cache)
      this.load()
    },
    async batchDetect() {
      const ids = this.selected.map(i => i.id)
      await handleReq(batchDetectImage({ ids }))
      this.$message.success('批量检测已提交')
      this.load()
    },
    async showResult(row) {
      this.current = row
      this.compareVisible = true
      this.detailVisible = true
      this.detail = { plates: [] }
      try {
        this.detail = await handleReq(getImageDetail(row.id))
      } catch (e) {
        this.detail = { plates: [] }
      }
    },
    preview(row) {
      this.current = row
      this.compareVisible = true
    },
    async remove(row) {
      await this.$confirm('确认删除该图片？', '提示', { type: 'warning' })
      await handleReq(deleteImage(row.id))
      this.$message.success('删除成功')
      this.load()
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
.thumb {
  width: 80px; height: 60px; object-fit: cover; border-radius: 6px; cursor: pointer;
}
.detail-wrap { padding: 0 20px 20px; }
.plate-item {
  background: #f8fafc;
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 12px;
}
.plate-title {
  font-weight: 700;
  margin-bottom: 10px;
  color: #1e40af;
}
</style>
