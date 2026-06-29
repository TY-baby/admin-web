<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">视频资源管理</div>
      <div class="hero-desc">统一管理原始视频与结果视频资产，支持筛选、批量下载与批量删除。</div>
    </div>

    <div class="plate-card">
      <div class="plate-toolbar">
        <div class="plate-actions">
          <el-input v-model="query.keyword" placeholder="文件名" clearable style="width:200px" />
          <el-date-picker v-model="query.range" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd" />
          <el-select v-model="query.status" placeholder="状态" clearable style="width:130px">
            <el-option label="已处理" value="detected" />
            <el-option label="未处理" value="pending" />
          </el-select>
          <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        </div>
        <div class="plate-actions">
          <el-button icon="el-icon-download" :disabled="!selected.length" @click="batchDownload">批量下载</el-button>
          <el-button icon="el-icon-delete" type="danger" plain :disabled="!selected.length" @click="batchRemove">批量删除</el-button>
        </div>
      </div>

      <el-table :data="list" v-loading="loading" border @selection-change="onSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="filename" label="文件名" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'detected' ? 'success' : 'info'">{{ scope.row.status === 'detected' ? '已处理' : '未处理' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="size" label="大小" width="100">
          <template slot-scope="scope">{{ formatSize(scope.row.size) }}</template>
        </el-table-column>
        <el-table-column prop="create_time" label="上传时间" width="180">
          <template slot-scope="scope">{{ formatDate(scope.row.create_time) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template slot-scope="scope">
            <el-button type="text" @click="preview(scope.row)">对比</el-button>
            <el-button type="text" @click="download(scope.row)">下载</el-button>
            <el-button type="text" style="color:#f56c6c" @click="remove(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog :visible.sync="compareVisible" title="原视频与结果视频" width="960px">
      <div class="plate-preview-grid" v-if="current">
        <div class="preview-panel">
          <div class="preview-label">原始视频</div>
          <video :src="current.url" controls class="preview-media"></video>
        </div>
        <div class="preview-panel">
          <div class="preview-label">结果视频</div>
          <video :src="current.result_url || current.url" controls class="preview-media"></video>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getVideoResourceList, deleteVideoBatch, downloadVideo } from '@/api/modules/plate'
import { formatDate, formatSize, handleReq, staticVideoUrl, downloadBlob } from './helpers'

export default {
  data() {
    return {
      loading: false,
      list: [],
      selected: [],
      query: { keyword: '', range: [], status: '' },
      compareVisible: false,
      current: null
    }
  },
  created() { this.load() },
  methods: {
    formatDate, formatSize,
    async load() {
      this.loading = true
      try {
        const data = await handleReq(getVideoResourceList(this.query))
        this.list = (data || []).map(item => ({
          ...item,
          url: staticVideoUrl(item.path),
          result_url: item.result_path ? staticVideoUrl(item.result_path) : ''
        }))
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
      const blob = await handleReq(downloadVideo(row.id), { raw: true })
      downloadBlob(blob, row.filename)
    },
    async batchDownload() {
      for (const row of this.selected) {
        await this.download(row)
      }
    },
    async remove(row) {
      await this.$confirm('确认删除？', '提示', { type: 'warning' })
      await handleReq(deleteVideoBatch({ ids: [row.id] }))
      this.$message.success('删除成功')
      this.load()
    },
    async batchRemove() {
      await this.$confirm('确认批量删除？', '提示', { type: 'warning' })
      const ids = this.selected.map(i => i.id)
      await handleReq(deleteVideoBatch({ ids }))
      this.$message.success('删除成功')
      this.selected = []
      this.load()
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
</style>
