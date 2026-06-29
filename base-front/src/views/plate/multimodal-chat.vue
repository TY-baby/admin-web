<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">多模态大模型聊天</div>
      <div class="hero-desc">在文本问答基础上增加图片上下文，可选择系统图片或上传本地图片进行视觉问答。</div>
    </div>

    <div class="plate-grid-2">
      <div class="plate-card chat-panel">
        <div class="chat-messages" ref="chatBox">
          <div v-for="(msg, i) in messages" :key="i" :class="['chat-msg', msg.role]">
            <div class="chat-bubble">
              <img v-if="msg.image" :src="msg.image" class="msg-image" />
              <div>{{ msg.content }}</div>
            </div>
          </div>
        </div>
        <div class="chat-input-area">
          <div v-if="selectedImage" class="selected-image">
            <img :src="selectedImage" />
            <i class="el-icon-close" @click="selectedImage=''"></i>
          </div>
          <el-input v-model="input" type="textarea" :rows="3" placeholder="输入问题..." @keydown.enter.native.prevent="send" />
          <div class="input-actions">
            <el-button icon="el-icon-picture" @click="imagePickerVisible=true">选择图片</el-button>
            <el-upload action="" :http-request="handleImageUpload" :show-file-list="false" accept="image/*">
              <el-button icon="el-icon-upload2">上传本地图片</el-button>
            </el-upload>
            <el-checkbox v-model="useStream">流式</el-checkbox>
            <el-button type="primary" icon="el-icon-s-promotion" :loading="sending" @click="send">发送</el-button>
            <el-button icon="el-icon-delete" @click="clear">清空</el-button>
          </div>
        </div>
      </div>

      <div class="plate-card">
        <div class="card-title">模型配置</div>
        <el-form label-width="90px">
          <el-form-item label="视觉模型">
            <el-select v-model="config.model" placeholder="请选择" style="width:100%">
              <el-option v-for="m in models" :key="m.id" :label="m.name" :value="m.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="温度">
            <el-slider v-model="config.temperature" :min="0" :max="1" :step="0.1" show-input />
          </el-form-item>
        </el-form>
        <div class="hint">提示：可结合图片询问“图中车牌是什么颜色？”或“识别结果是否准确？”。</div>
      </div>
    </div>

    <el-dialog :visible.sync="imagePickerVisible" title="选择系统图片" width="700px">
      <div class="image-grid">
        <div v-for="img in images" :key="img.id" class="image-item" @click="pickImage(img)">
          <img :src="img.url" />
          <div class="image-name">{{ img.filename }}</div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getVisionModels, chatVision, chatVisionStream } from '@/api/modules/plate'
import { getImageResourceList } from '@/api/modules/plate'
import { handleReq, staticImageUrl, getMultimodalContext, setMultimodalContext } from './helpers'

export default {
  data() {
    return {
      models: [],
      config: { model: '', temperature: 0.7 },
      messages: [],
      input: '',
      sending: false,
      useStream: true,
      selectedImage: '',
      imagePickerVisible: false,
      images: []
    }
  },
  async created() {
    this.messages = getMultimodalContext()
    if (!this.messages.length) {
      this.messages = [{ role: 'assistant', content: '你好，我可以结合图片回答你的问题。' }]
    }
    try {
      this.models = await handleReq(getVisionModels())
      if (this.models.length) this.config.model = this.models[0].id
      const imgs = await handleReq(getImageResourceList({ limit: 50 }))
      this.images = (imgs || []).map(i => ({ ...i, url: staticImageUrl(i.path) }))
    } catch (e) {
      console.warn('初始化失败', e)
    }
  },
  updated() { this.scrollToBottom() },
  beforeDestroy() { setMultimodalContext(this.messages) },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const box = this.$refs.chatBox
        if (box) box.scrollTop = box.scrollHeight
      })
    },
    pickImage(img) {
      this.selectedImage = img.url
      this.imagePickerVisible = false
    },
    async handleImageUpload({ file }) {
      const reader = new FileReader()
      reader.onload = e => { this.selectedImage = e.target.result }
      reader.readAsDataURL(file)
    },
    async send() {
      if (!this.input.trim() && !this.selectedImage) return
      if (!this.config.model) return this.$message.warning('请选择模型')
      const text = this.input.trim()
      this.messages.push({ role: 'user', content: text, image: this.selectedImage })
      this.input = ''
      this.sending = true
      try {
        const payload = { ...this.config, message: text, image: this.selectedImage }
        if (this.useStream) {
          await this.streamChat(payload)
        } else {
          const res = await handleReq(chatVision(payload))
          this.messages.push({ role: 'assistant', content: res.reply || res.content })
        }
      } catch (e) {
        this.$message.error('请求失败')
      } finally {
        this.sending = false
        this.selectedImage = ''
      }
    },
    async streamChat(payload) {
      const base = process.env.VUE_APP_BASE_API || '/api'
      const token = localStorage.getItem('base_token')
      const res = await fetch(base + '/plate/vision/chat-stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: 'Bearer ' + token } : {}) },
        body: JSON.stringify(payload)
      })
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let reply = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        reply += decoder.decode(value, { stream: true })
      }
      this.messages.push({ role: 'assistant', content: reply })
    },
    clear() {
      this.messages = [{ role: 'assistant', content: '会话已清空。' }]
      setMultimodalContext(this.messages)
    }
  }
}
</script>

<style lang="scss" scoped>
@import './page.scss';
.chat-panel { display: flex; flex-direction: column; height: calc(100vh - 240px); }
.chat-messages { flex: 1; overflow-y: auto; padding: 10px; background: #f8fafc; border-radius: 12px; margin-bottom: 12px; }
.chat-msg { margin-bottom: 12px; display: flex; }
.chat-msg.user { justify-content: flex-end; }
.chat-bubble {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
  background: #fff;
  color: #1e293b;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.chat-msg.user .chat-bubble { background: linear-gradient(135deg, #4f46e5, #6366f1); color: #fff; }
.msg-image { max-width: 200px; max-height: 150px; border-radius: 8px; margin-bottom: 8px; display: block; }
.selected-image {
  position: relative; display: inline-block; margin-bottom: 8px;
  img { max-width: 120px; max-height: 90px; border-radius: 8px; }
  i { position: absolute; top: -6px; right: -6px; background: #f56c6c; color: #fff; border-radius: 50%; width: 18px; height: 18px; display: flex; align-items: center; justify-content: center; font-size: 12px; cursor: pointer; }
}
.input-actions { display: flex; align-items: center; justify-content: flex-end; gap: 10px; margin-top: 10px; flex-wrap: wrap; }
.card-title { font-size: 16px; font-weight: 700; margin-bottom: 16px; }
.hint { margin-top: 20px; font-size: 13px; color: #94a3b8; line-height: 1.6; }
.image-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.image-item { background: #f8fafc; border-radius: 8px; padding: 8px; text-align: center; cursor: pointer; }
.image-item img { width: 100%; height: 120px; object-fit: cover; border-radius: 6px; }
.image-name { font-size: 12px; color: #64748b; margin-top: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
