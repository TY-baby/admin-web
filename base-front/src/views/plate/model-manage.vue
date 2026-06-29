<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">模型管理</div>
      <div class="hero-desc">管理检测与识别模型元数据，支持模型上传、编辑、加载与详情查看。</div>
    </div>

    <div class="plate-card">
      <div class="plate-toolbar">
        <div class="plate-actions">
          <el-button type="primary" icon="el-icon-upload2" @click="uploadVisible=true">上传模型</el-button>
          <el-button icon="el-icon-refresh" @click="load">刷新</el-button>
        </div>
      </div>

      <el-table :data="list" v-loading="loading" border>
        <el-table-column prop="filename" label="模型文件名" />
        <el-table-column prop="name" label="模型名称" />
        <el-table-column prop="dataset" label="数据集" />
        <el-table-column prop="base_model" label="基础模型" />
        <el-table-column prop="version" label="版本号" width="100" />
        <el-table-column prop="accuracy" label="准确率" width="100">
          <template slot-scope="scope">{{ formatPercent(scope.row.accuracy) }}</template>
        </el-table-column>
        <el-table-column prop="upload_time" label="上传时间" width="160">
          <template slot-scope="scope">{{ formatDate(scope.row.upload_time) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="160">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.is_default" type="warning" size="mini">默认模型</el-tag>
            <el-tag v-if="scope.row.is_loaded" type="success" size="mini" style="margin-left:4px">已加载</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template slot-scope="scope">
            <el-button type="text" @click="showDetail(scope.row)">详情</el-button>
            <el-button type="text" @click="openEdit(scope.row)">编辑</el-button>
            <el-button type="text" @click="loadModel(scope.row)">加载</el-button>
            <el-button type="text" style="color:#f56c6c" @click="remove(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog :visible.sync="uploadVisible" title="上传模型" width="500px">
      <el-form label-width="80px">
        <el-form-item label="模型文件">
          <el-upload action="" :http-request="handleUpload" :show-file-list="false" accept=".pt,.pth,.onnx">
            <el-button type="primary">选择文件</el-button>
          </el-upload>
          <div v-if="uploadFileName" class="file-name">{{ uploadFileName }}</div>
        </el-form-item>
      </el-form>
      <div slot="footer"><el-button @click="uploadVisible=false">取消</el-button></div>
    </el-dialog>

    <el-dialog :visible.sync="editVisible" title="编辑模型" width="600px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="模型名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="数据集"><el-input v-model="form.dataset" /></el-form-item>
        <el-form-item label="基础模型"><el-input v-model="form.base_model" /></el-form-item>
        <el-form-item label="版本号"><el-input v-model="form.version" /></el-form-item>
        <el-form-item label="准确率"><el-input v-model="form.accuracy" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" /></el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="editVisible=false">取消</el-button>
        <el-button type="primary" @click="submitEdit">保存</el-button>
      </div>
    </el-dialog>

    <el-drawer :visible.sync="detailVisible" title="模型详情" size="420px">
      <div v-if="current" class="detail-wrap">
        <div class="plate-kv">
          <span class="kv-label">模型文件名</span><span class="kv-value">{{ current.filename }}</span>
          <span class="kv-label">模型名称</span><span class="kv-value">{{ current.name }}</span>
          <span class="kv-label">数据集</span><span class="kv-value">{{ current.dataset }}</span>
          <span class="kv-label">基础模型</span><span class="kv-value">{{ current.base_model }}</span>
          <span class="kv-label">版本号</span><span class="kv-value">{{ current.version }}</span>
          <span class="kv-label">准确率</span><span class="kv-value">{{ formatPercent(current.accuracy) }}</span>
          <span class="kv-label">上传时间</span><span class="kv-value">{{ formatDate(current.upload_time) }}</span>
          <span class="kv-label">是否默认</span><span class="kv-value">{{ current.is_default ? '是' : '否' }}</span>
          <span class="kv-label">是否加载</span><span class="kv-value">{{ current.is_loaded ? '是' : '否' }}</span>
          <span class="kv-label">描述</span><span class="kv-value">{{ current.description || '-' }}</span>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import { getModelList, uploadModel, updateModel, loadModel, deleteModel } from '@/api/modules/plate'
import { formatDate, formatPercent, handleReq } from './helpers'

export default {
  data() {
    return {
      loading: false,
      list: [],
      uploadVisible: false,
      editVisible: false,
      detailVisible: false,
      current: null,
      form: {},
      uploadFileName: ''
    }
  },
  created() { this.load() },
  methods: {
    formatDate, formatPercent,
    async load() {
      this.loading = true
      try {
        this.list = await handleReq(getModelList())
      } finally {
        this.loading = false
      }
    },
    async handleUpload({ file }) {
      const fd = new FormData()
      fd.append('file', file)
      await handleReq(uploadModel(fd))
      this.$message.success('上传成功')
      this.uploadVisible = false
      this.uploadFileName = ''
      this.load()
    },
    showDetail(row) {
      this.current = row
      this.detailVisible = true
    },
    openEdit(row) {
      this.form = { ...row }
      this.editVisible = true
    },
    async submitEdit() {
      await handleReq(updateModel(this.form.id, this.form))
      this.$message.success('保存成功')
      this.editVisible = false
      this.load()
    },
    async loadModel(row) {
      await handleReq(loadModel(row.id))
      this.$message.success('模型加载成功')
      this.load()
    },
    async remove(row) {
      await this.$confirm('确认删除该模型？', '提示', { type: 'warning' })
      await handleReq(deleteModel(row.id))
      this.$message.success('删除成功')
      this.load()
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
.file-name { margin-top: 8px; font-size: 13px; color: #64748b; }
.detail-wrap { padding: 0 20px 20px; }
</style>
