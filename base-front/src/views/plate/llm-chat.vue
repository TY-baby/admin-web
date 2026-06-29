<template>
  <div class="plate-page">
    <div class="plate-hero">
      <div class="hero-title">大模型聊天</div>
      <div class="hero-desc">选择文本模型、配置参数，以普通或流式方式获取模型回复，辅助解读检测结果。</div>
    </div>

    <div class="plate-grid-2">
      <div class="plate-card chat-panel">
        <div class="chat-messages" ref="chatBox">
          <div v-for="(msg, i) in messages" :key="i" :class="['chat-msg', msg.role]">
            <div class="chat-bubble">{{ msg.content }}</div>
          </div>
          <div v-if="streaming" class="chat-msg assistant">
            <div class="chat-bubble">{{ streamText }}<span class="cursor">|</span></div>
          </div>
        </div>
        <div class="chat-input-area">
          <el-input v-model="input" type="textarea" :rows="3" placeholder="输入问题..." @keydown.enter.native.prevent="send" />
          <div class="input-actions">
            <el-checkbox v-model="useStream">流式输出</el-checkbox>
            <el-button type="primary" icon="el-icon-s-promotion" :loading="sending" @click="send">发送</el-button>
            <el-button icon="el-icon-delete" @click="clear">清空</el-button>
          </div>
        </div>
      </div>

      <div class="plate-card">
        <div class="card-title">模型配置</div>
        <el-form label-width="90px">
          <el-form-item label="选择模型">
            <el-select v-model="config.model" placeholder="请选择" style="width:100%">
              <el-option v-for="m in models" :key="m.id" :label="m.name" :value="m.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="温度">
            <el-slider v-model="config.temperature" :min="0" :max="1" :step="0.1" show-input />
          </el-form-item>
          <el-form-item label="最大令牌">
            <el-input-number v-model="config.max_tokens" :min="100" :max="4096" style="width:100%" />
          </el-form-item>
        </el-form>
        <div class="hint">提示：可询问“帮我总结最近的检测记录”或“解读京 A12345 的识别结果”。</div>
      </div>
    </div>
  </div>
</template>

<script>
import { getTextModels, chatText, chatTextStream } from '@/api/modules/plate'
import { handleReq } from './helpers'

export default {
  data() {
    return {
      models: [],
      config: { model: '', temperature: 0.7, max_tokens: 1024 },
      messages: [{ role: 'assistant', content: '你好，我是车牌识别助手，请问有什么可以帮到你？' }],
      input: '',
      sending: false,
      useStream: true,
      streaming: false,
      streamText: ''
    }
  },
  async created() {
    try {
      this.models = await handleReq(getTextModels())
      if (this.models.length) this.config.model = this.models[0].id
    } catch (e) {
      console.warn('模型加载失败', e)
    }
  },
  updated() { this.scrollToBottom() },
  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const box = this.$refs.chatBox
        if (box) box.scrollTop = box.scrollHeight
      })
    },
    async send() {
      if (!this.input.trim()) return
      if (!this.config.model) return this.$message.warning('请选择模型')
      const text = this.input.trim()
      this.messages.push({ role: 'user', content: text })
      this.input = ''
      this.sending = true

      try {
        if (this.useStream) {
          await this.streamChat(text)
        } else {
          const res = await handleReq(chatText({ ...this.config, message: text }))
          this.messages.push({ role: 'assistant', content: res.reply || res.content })
        }
      } catch (e) {
        this.$message.error('请求失败')
      } finally {
        this.sending = false
      }
    },
    async streamChat(text) {
      this.streaming = true
      this.streamText = ''
      const base = process.env.VUE_APP_BASE_API || '/api'
      const token = localStorage.getItem('base_token')
      const res = await fetch(base + '/plate/llm/chat-stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: 'Bearer ' + token } : {}) },
        body: JSON.stringify({ ...this.config, message: text })
      })
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        this.streamText += decoder.decode(value, { stream: true })
      }
      this.messages.push({ role: 'assistant', content: this.streamText })
      this.streaming = false
      this.streamText = ''
    },
    clear() {
      this.messages = [{ role: 'assistant', content: '会话已清空，请问有什么可以帮到你？' }]
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
.chat-msg.assistant .chat-bubble { background: #fff; }
.cursor { animation: blink 1s infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
.input-actions { display: flex; align-items: center; justify-content: flex-end; gap: 10px; margin-top: 10px; }
.card-title { font-size: 16px; font-weight: 700; margin-bottom: 16px; }
.hint { margin-top: 20px; font-size: 13px; color: #94a3b8; line-height: 1.6; }
</style>
