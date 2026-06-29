<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">图片资源管理</div>
      <div class="hero-desc">集中管理原始图片与检测结果图，支持检索、下载、删除与联动查看。</div>
    </div>

    <div class="plate-card">
      <div class="plate-toolbar">
        <div class="plate-actions">
          <el-input v-model="query.keyword" placeholder="文件名" clearable style="width:200px" />
          <el-date-picker v-model="query.range" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd" />
          <el-select v-model="query.status" placeholder="检测状态" clearable style="width:130px">
            <el-option label="已检测" value="detected" />
            <el-option label="未检测" value="pending" />
          </el-select>
          <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        </div>
        <div class="plate-actions">
          <el-button icon="el-icon-s-grid" :type="viewMode === 'grid' ? 'primary' : 'default'" @click="viewMode='grid'">缩略图</el-button>
          <el-button icon="el-icon-s-unfold" :type="viewMode === 'table' ? 'primary' : 'default'" @click="viewMode='table'">表格</el-button>
        </div>
      </div>

      <div v-if="viewMode === 'grid'" class="plate-grid-4">
        <div class="plate-card image-card" v-for="item in list" :key="item.id">
          <img :src="item.url" class="card-image" @click="preview(item)" />
          <div class="card-info">
            <div class="card-name" :title="item.filename">{{ item.filename }}</div>
            <el-tag size="mini" :type="item.status === 'detected' ? 'success' : 'info'">
              {{ item.status === 'detected' ? '已检测' : '未检测' }}
            </el-tag>
          </div>
          <div class="card-actions">
            <el-button type="text" @click="download(item)">下载</el-button>
            <el-button type="text" style="color:#f56c6c" @click="remove(item)">删除</el-button>
          </div>
        </div>
      </div>

      <el-table v-else :data="list" v-loading="loading" border @selection-change="onSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="filename" label="文件名" />
        <el-table-column label="缩略图" width="120">
          <template slot-scope="scope"><img :src="scope.row.url" class="thumb" @click="preview(scope.row)" /></template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'detected' ? 'success' : 'info'">{{ scope.row.status === 'detected' ? '已检测' : '未检测' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="上传时间" width="180">
          <template slot-scope="scope">{{ formatDate(scope.row.create_time) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template slot-scope="scope">
            <el-button type="text" @click="download(scope.row)">下载</el-button>
            <el-button type="text" style="color:#f56c6c" @click="remove(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog :visible.sync="compareVisible" title="原图与结果图" width="900px">
      <div class="plate-preview-grid" v-if="current">
        <div class="preview-panel">
          <div class="preview-label">原始图片</div>
          <img :src="current.url" class="preview-media" />
        </div>
        <div class="preview-panel">
          <div class="preview-label">结果图片</div>
          <img :src="current.result_url || current.url" class="preview-media" />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getImageResourceList, deleteImageBatch, downloadImage } from '@/api/modules/plate'
import { formatDate, handleReq, staticImageUrl, downloadBlob } from './helpers'

export default {
  data() {
    return {
      loading: false,
      viewMode: 'grid',
      list: [],
      selected: [],
      query: { keyword: '', range: [], status: '' },
      compareVisible: false,
      current: null
    }
  },
  created() { this.load() },
  methods: {
    formatDate,
    async load() {
      this.loading = true
      try {
        const data = await handleReq(getImageResourceList(this.query))
        this.list = (data || []).map(item => ({ ...item, url: staticImageUrl(item.path) }))
      } finally {
        this.loading = false
      }
    },
    onSelectionChange(rows) { this.selected = rows },
    preview(row) {
      this.current = row
      this.compareVisible = true
    },
    async download(row) {
      const blob = await handleReq(downloadImage(row.id), { raw: true })
      downloadBlob(blob, row.filename)
    },
    async remove(row) {
      await this.$confirm('确认删除？', '提示', { type: 'warning' })
      await handleReq(deleteImageBatch({ ids: [row.id] }))
      this.$message.success('删除成功')
      this.load()
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
.thumb { width: 80px; height: 60px; object-fit: cover; border-radius: 6px; cursor: pointer; }
.image-card {
  padding: 12px;
  text-align: center;
}
.card-image {
  width: 100%; height: 140px; object-fit: cover; border-radius: 8px; cursor: pointer; margin-bottom: 10px;
}
.card-info {
  display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;
}
.card-name {
  font-size: 13px; color: #1e293b; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 70%;
}
.card-actions {
  display: flex; justify-content: center; gap: 12px;
}
</style>
