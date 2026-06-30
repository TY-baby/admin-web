<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">视频车牌检测识别</div>
      <div class="hero-desc">支持原始视频上传、批量检测与帧级识别记录查看，结果视频可在线播放。</div>
    </div>

    <div class="plate-card">
      <div class="plate-toolbar">
        <div class="plate-actions">
          <el-upload action="" :http-request="handleUpload" :show-file-list="false" accept="video/*">
            <el-button type="primary" icon="el-icon-upload2">上传视频</el-button>
          </el-upload>
          <el-button type="success" icon="el-icon-cpu" :disabled="!selected.length" @click="batchDetect">批量检测</el-button>
          <el-button icon="el-icon-refresh" @click="load">刷新列表</el-button>
        </div>
      </div>

      <el-table :data="list" v-loading="loading" border @selection-change="onSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="filename" label="文件名" />
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'detected' ? 'success' : 'info'">
              {{ scope.row.status === 'detected' ? '已处理' : '未处理' }}
            </el-tag>
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
            <el-button type="text" @click="detect(scope.row)">检测</el-button>
            <el-button type="text" :disabled="scope.row.status !== 'detected'" @click="showResult(scope.row)">结果</el-button>
            <el-button type="text" style="color:#f56c6c" @click="remove(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog :visible.sync="compareVisible" title="原视频与结果对比" width="960px">
      <div class="plate-preview-grid" v-if="current">
        <div class="preview-panel">
          <div class="preview-label">原始视频</div>
          <video :src="current.url" controls class="preview-media"></video>
        </div>
        <div class="preview-panel">
          <div class="preview-label">检测结果</div>
          <video :src="current.result_url || current.url" controls class="preview-media"></video>
          <el-alert v-if="compatTip" :title="compatTip" type="warning" :closable="false" style="margin-top:10px" />
        </div>
      </div>
    </el-dialog>

    <el-drawer :visible.sync="frameVisible" title="帧级识别记录" size="560px">
      <el-table :data="frames" height="calc(100vh - 140px)" border>
        <el-table-column prop="frame_no" label="帧号" width="80" />
        <el-table-column prop="timestamp" label="时间戳" width="100" />
        <el-table-column prop="plate_no" label="车牌号" />
        <el-table-column prop="confidence" label="置信度">
          <template slot-scope="scope">{{ formatPercent(scope.row.confidence) }}</template>
        </el-table-column>
      </el-table>
    </el-drawer>
  </div>
</template>

<script>
import {
  getVideoList, uploadVideo, detectVideo, batchDetectVideo, deleteVideo, getVideoDetail
} from '@/api/modules/plate'
import {
  formatDate, formatSize, formatPercent, getVideoCache, setVideoCache,
  handleReq, staticVideoUrl
} from './helpers'

export default {
  data() {
    return {
      loading: false,
      list: [],
      selected: [],
      compareVisible: false,
      frameVisible: false,
      current: null,
      frames: [],
      compatTip: ''
    }
  },
  created() { this.load() },
  methods: {
    formatDate, formatSize, formatPercent,
    async load() {
      this.loading = true
      try {
        const data = await handleReq(getVideoList())
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
    async handleUpload({ file }) {
      const fd = new FormData()
      fd.append('file', file)
      await handleReq(uploadVideo(fd))
      this.$message.success('上传成功')
      this.load()
    },
    async detect(row) {
      const res = await handleReq(detectVideo({ id: row.id }))
      this.$message.success('检测完成')
      row.status = 'detected'
      row.result_path = res.result_path
      row.result_url = staticVideoUrl(res.result_path)
      const cache = getVideoCache()
      cache[row.id] = res
      setVideoCache(cache)
      this.load()
    },
    async batchDetect() {
      const ids = this.selected.map(i => i.id)
      await handleReq(batchDetectVideo({ ids }))
      this.$message.success('批量检测已提交')
      this.load()
    },
    async showResult(row) {
      this.current = row
      this.compareVisible = true
      this.frameVisible = true
      this.frames = []
      this.compatTip = ''
      try {
        const detail = await handleReq(getVideoDetail(row.id))
        this.frames = detail.frames || []
        const codec = detail.video_codec || row.video_codec
        const transcoded = detail.transcoded || row.transcoded
        this.compatTip = codec && codec !== 'h264' && !transcoded
          ? '当前视频编码为 ' + codec + '，部分浏览器可能无法直接播放，建议后端转码为 H.264'
          : ''
      } catch (e) {
        this.frames = []
      }
    },
    async remove(row) {
      await this.$confirm('确认删除该视频？', '提示', { type: 'warning' })
      await handleReq(deleteVideo(row.id))
      this.$message.success('删除成功')
      this.load()
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
</style>
