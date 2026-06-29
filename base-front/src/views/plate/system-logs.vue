<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">系统日志</div>
      <div class="hero-desc">查看日志文件列表、快速预览内容，支持关键字过滤、复制、下载与删除。</div>
    </div>

    <div class="plate-card">
      <div class="plate-toolbar">
        <div class="plate-actions">
          <el-input v-model="query.keyword" placeholder="关键字过滤" clearable style="width:220px" />
          <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        </div>
        <div class="plate-actions">
          <el-button icon="el-icon-download" :disabled="!selected.length" @click="batchDownload">批量下载</el-button>
          <el-button icon="el-icon-delete" type="danger" plain :disabled="!selected.length" @click="batchRemove">批量删除</el-button>
        </div>
      </div>

      <el-table :data="list" v-loading="loading" border @selection-change="onSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="文件名" />
        <el-table-column prop="size" label="大小" width="100">
          <template slot-scope="scope">{{ formatSize(scope.row.size) }}</template>
        </el-table-column>
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <el-tag v-if="isToday(scope.row.date)" type="warning" size="mini">使用中</el-tag>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template slot-scope="scope">
            <el-button type="text" @click="preview(scope.row)">预览</el-button>
            <el-button type="text" @click="download(scope.row)">下载</el-button>
            <el-button type="text" :disabled="isToday(scope.row.date)" style="color:#f56c6c" @click="remove(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog :visible.sync="previewVisible" title="日志预览" width="800px">
      <el-input v-model="filterText" placeholder="内容过滤" clearable size="small" style="margin-bottom:10px" />
      <pre class="log-content">{{ filteredContent }}</pre>
      <div slot="footer">
        <el-button @click="copyContent">复制当前内容</el-button>
        <el-button type="primary" @click="previewVisible=false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getLogList, previewLog, downloadLog, deleteLog } from '@/api/modules/plate'
import { formatSize, formatDate, handleReq, downloadBlob } from './helpers'

export default {
  data() {
    return {
      loading: false,
      list: [],
      selected: [],
      query: { keyword: '' },
      previewVisible: false,
      current: null,
      content: '',
      filterText: ''
    }
  },
  computed: {
    filteredContent() {
      if (!this.filterText) return this.content
      const lines = this.content.split('\n')
      return lines.filter(l => l.includes(this.filterText)).join('\n')
    }
  },
  created() { this.load() },
  methods: {
    formatSize, formatDate,
    isToday(dateStr) {
      return dateStr === formatDate(new Date(), 'YYYY-MM-DD')
    },
    async load() {
      this.loading = true
      try {
        this.list = await handleReq(getLogList(this.query))
      } finally {
        this.loading = false
      }
    },
    onSelectionChange(rows) { this.selected = rows },
    async preview(row) {
      this.current = row
      this.content = await handleReq(previewLog({ name: row.name, lines: 200 }))
      this.previewVisible = true
    },
    async download(row) {
      const blob = await handleReq(downloadLog(row.name), { raw: true })
      downloadBlob(blob, row.name)
    },
    async batchDownload() {
      for (const row of this.selected) await this.download(row)
    },
    async remove(row) {
      if (this.isToday(row.date)) return this.$message.warning('当天日志不可删除')
      await this.$confirm('确认删除？', '提示', { type: 'warning' })
      await handleReq(deleteLog(row.name))
      this.$message.success('删除成功')
      this.load()
    },
    async batchRemove() {
      const today = this.selected.some(r => this.isToday(r.date))
      if (today) return this.$message.warning('选中项包含当天日志，不可删除')
      await this.$confirm('确认批量删除？', '提示', { type: 'warning' })
      for (const row of this.selected) await handleReq(deleteLog(row.name))
      this.$message.success('删除成功')
      this.selected = []
      this.load()
    },
    copyContent() {
      navigator.clipboard.writeText(this.filteredContent).then(() => {
        this.$message.success('已复制')
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
.log-content {
  background: #0f172a;
  color: #e2e8f0;
  padding: 16px;
  border-radius: 10px;
  max-height: 400px;
  overflow: auto;
  font-size: 12px;
  line-height: 1.6;
  white-space: pre-wrap;
}
.text-muted { color: #94a3b8; }
</style>
