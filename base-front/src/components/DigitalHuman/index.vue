<template>
  <div class="digital-human">
    <!-- 悬浮入口 -->
    <div class="dh-avatar-wrap" @click="togglePanel">
      <div class="dh-avatar" :class="{ talking: isSpeaking }">
        <div class="dh-face">
          <div class="dh-eyes">
            <div class="dh-eye"></div>
            <div class="dh-eye"></div>
          </div>
          <div class="dh-mouth" :class="{ open: isSpeaking }"></div>
        </div>
        <div class="dh-ring"></div>
        <div class="dh-ring delay"></div>
      </div>
      <div v-if="showBadge" class="dh-badge">{{ unread }}</div>
    </div>

    <!-- 对话面板 -->
    <el-drawer
      :visible.sync="visible"
      direction="rtl"
      :show-close="false"
      :size="420"
      :append-to-body="true"
      :modal-append-to-body="true"
      class="dh-drawer"
      @opened="onOpened"
    >
      <div class="dh-panel">
        <!-- 头部 -->
        <div class="dh-header">
          <div class="dh-header-left">
            <div class="dh-avatar-mini">
              <div class="dh-face-mini">
                <div class="dh-eyes-mini">
                  <div></div><div></div>
                </div>
                <div class="dh-mouth-mini"></div>
              </div>
            </div>
            <div>
              <div class="dh-name">小 Base</div>
              <div class="dh-status">
                <span class="dh-dot"></span> AI 流程助手
              </div>
            </div>
          </div>
          <div class="dh-header-actions">
            <el-tooltip content="语音播报" placement="bottom">
              <i
                :class="voiceEnabled ? 'el-icon-microphone' : 'el-icon-turn-off-microphone'"
                class="dh-action-icon"
                @click="voiceEnabled = !voiceEnabled"
              />
            </el-tooltip>
            <i class="el-icon-close dh-action-icon" @click="visible = false" />
          </div>
        </div>

        <!-- 消息区 -->
        <div ref="messageBox" class="dh-messages">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="dh-message"
            :class="msg.role"
          >
            <div class="dh-bubble">
              <div v-if="msg.guide" class="dh-guide">
                <div class="dh-guide-title">{{ msg.guide.title }}</div>
                <div class="dh-guide-steps">
                  <div v-for="(step, si) in msg.guide.steps" :key="si" class="dh-step">
                    <span class="dh-step-num">{{ si + 1 }}</span>
                    <span class="dh-step-text">{{ step }}</span>
                  </div>
                </div>
                <el-button
                  v-if="msg.guide.link"
                  type="primary"
                  size="mini"
                  @click="goTo(msg.guide.link)"
                >去操作</el-button>
              </div>
              <div v-else class="dh-text" v-html="formatText(msg.content)"></div>
              <div v-if="msg.quickActions && msg.quickActions.length" class="dh-quick-actions">
                <el-button
                  v-for="(action, ai) in msg.quickActions"
                  :key="ai"
                  size="mini"
                  round
                  @click="handleQuick(action)"
                >{{ action.label }}</el-button>
              </div>
            </div>
            <div class="dh-time">{{ msg.time }}</div>
          </div>

          <div v-if="loading" class="dh-message assistant">
            <div class="dh-bubble dh-typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>

        <!-- 快捷问题 -->
        <div class="dh-chips">
          <span
            v-for="(chip, ci) in chips"
            :key="ci"
            class="dh-chip"
            @click="handleChip(chip)"
          >{{ chip.label }}</span>
        </div>

        <!-- 输入区 -->
        <div class="dh-input-area">
          <el-input
            v-model="input"
            placeholder="输入问题，或点击下方快捷引导"
            size="medium"
            @keyup.enter.native="send"
          />
          <el-button type="primary" icon="el-icon-s-promotion" :loading="loading" @click="send" />
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import { chatText } from '@/api/modules/plate'

const GUIDES = {
  'plate-image': {
    title: '图片车牌检测流程',
    steps: [
      '进入「车牌识别 → 图片车牌检测」页面',
      '点击「上传图片」按钮，选择需要识别的车辆图片',
      '上传成功后，列表会显示该图片，点击「检测」按钮',
      '等待系统完成识别，状态变为「已检测」',
      '点击「结果」按钮，查看识别明细（车牌号、颜色、置信度等）'
    ],
    link: '/plate/image-detect'
  },
  'plate-video': {
    title: '视频车牌检测流程',
    steps: [
      '进入「车牌识别 → 视频车牌检测」页面',
      '上传包含车辆的本地视频文件',
      '点击「检测」按钮，系统会逐帧分析',
      '检测完成后，点击「结果」查看帧级识别记录',
      '可在「视频资源管理」中下载或删除原视频'
    ],
    link: '/plate/video-detect'
  },
  'crm-customer': {
    title: 'CRM 客户管理流程',
    steps: [
      '点击左侧「CRM → 客户管理」菜单',
      '在客户列表页点击「新增客户」或「编辑」',
      '填写客户基础信息、联系人、等级等字段',
      '在客户详情页可查看商机、订单、跟进记录',
      '通过「跟进记录」模块持续维护客户关系'
    ],
    link: '/crm/customer'
  },
  'crm-order': {
    title: 'CRM 订单管理流程',
    steps: [
      '进入「CRM → 订单管理」页面',
      '点击「新增订单」，选择关联客户与产品',
      '填写金额、数量、交付日期等订单信息',
      '提交后可在列表查看订单状态',
      '订单详情页支持编辑、关闭及导出操作'
    ],
    link: '/crm/order'
  },
  'erp-purchase': {
    title: 'ERP 采购管理流程',
    steps: [
      '进入「ERP → 采购管理」页面',
      '点击「新增采购单」，选择供应商与物料',
      '填写采购数量、单价、到货日期',
      '提交后进入审批/待发货状态',
      '到货后在系统中确认入库，同步更新库存'
    ],
    link: '/erp/purchase'
  },
  'oa-leave': {
    title: 'OA 请假审批流程',
    steps: [
      '点击左侧「OA → 请假审批」菜单',
      '点击「我要请假」，选择请假类型与时间',
      '填写请假原因，提交申请',
      '直属领导在列表中收到待审批记录',
      '审批通过后，考勤系统会自动扣减假期余额'
    ],
    link: '/oa/leave'
  },
  'oa-expense': {
    title: 'OA 费用报销流程',
    steps: [
      '进入「OA → 费用报销」页面',
      '点击「新增报销」，选择报销类型',
      '上传发票图片，填写金额与事由',
      '提交后等待财务/领导审批',
      '审批通过后，财务统一打款并标记已支付'
    ],
    link: '/oa/expense'
  }
}

const CHIPS = [
  { label: '图片车牌检测', guide: 'plate-image' },
  { label: '视频车牌检测', guide: 'plate-video' },
  { label: 'CRM客户管理', guide: 'crm-customer' },
  { label: 'CRM订单管理', guide: 'crm-order' },
  { label: 'ERP采购流程', guide: 'erp-purchase' },
  { label: 'OA请假审批', guide: 'oa-leave' },
  { label: 'OA费用报销', guide: 'oa-expense' }
]

export default {
  name: 'DigitalHuman',
  data() {
    return {
      visible: false,
      input: '',
      loading: false,
      voiceEnabled: true,
      isSpeaking: false,
      unread: 1,
      messages: []
    }
  },
  computed: {
    showBadge() {
      return !this.visible && this.unread > 0
    },
    chips() {
      return CHIPS
    }
  },
  created() {
    this.pushWelcome()
  },
  methods: {
    togglePanel() {
      this.visible = !this.visible
      if (this.visible) this.unread = 0
    },
    onOpened() {
      this.scrollToBottom()
    },
    pushWelcome() {
      this.messages.push({
        role: 'assistant',
        content: '你好，我是小 Base，你的 AI 流程助手。我可以帮你引导车牌识别、CRM、ERP、OA 等系统操作。点击上方快捷问题，或直接输入你想了解的流程。',
        time: this.now(),
        quickActions: [
          { label: '图片车牌检测', guide: 'plate-image' },
          { label: 'CRM客户管理', guide: 'crm-customer' },
          { label: 'OA请假审批', guide: 'oa-leave' }
        ]
      })
    },
    handleChip(chip) {
      this.sendGuide(chip.guide)
    },
    handleQuick(action) {
      this.sendGuide(action.guide)
    },
    sendGuide(key) {
      const guide = GUIDES[key]
      if (!guide) return
      this.messages.push({ role: 'user', content: `查看「${guide.title}」`, time: this.now() })
      this.messages.push({ role: 'assistant', guide, time: this.now() })
      this.speak(`以下是${guide.title}的引导步骤`)
      this.scrollToBottom()
    },
    async send() {
      const text = this.input.trim()
      if (!text || this.loading) return
      this.messages.push({ role: 'user', content: text, time: this.now() })
      this.input = ''
      this.loading = true
      this.scrollToBottom()

      // 优先匹配本地流程引导
      const matched = this.matchGuide(text)
      if (matched) {
        this.messages.push({ role: 'assistant', guide: matched, time: this.now() })
        this.speak(`以下是${matched.title}的引导步骤`)
      } else {
        try {
          const res = await chatText({ message: text })
          const reply = res?.reply || res?.data?.reply || '抱歉，我暂时无法回答这个问题。'
          this.messages.push({ role: 'assistant', content: reply, time: this.now() })
          this.speak(reply)
        } catch (e) {
          this.messages.push({
            role: 'assistant',
            content: '网络有点问题，请稍后再试。你也可以点击上方快捷问题获取流程引导。',
            time: this.now()
          })
        }
      }
      this.loading = false
      this.scrollToBottom()
    },
    matchGuide(text) {
      const map = [
        { keys: ['图片', '图像', '照片', 'image'], guide: 'plate-image' },
        { keys: ['视频', '录像', 'video'], guide: 'plate-video' },
        { keys: ['客户', 'crm', 'CRM'], guide: 'crm-customer' },
        { keys: ['订单', '下单', 'order'], guide: 'crm-order' },
        { keys: ['采购', '进货', 'purchase'], guide: 'erp-purchase' },
        { keys: ['请假', '休假', 'leave'], guide: 'oa-leave' },
        { keys: ['报销', '费用', 'expense'], guide: 'oa-expense' }
      ]
      for (const item of map) {
        if (item.keys.some(k => text.toLowerCase().includes(k))) {
          return GUIDES[item.guide]
        }
      }
      return null
    },
    speak(text) {
      if (!this.voiceEnabled || !window.speechSynthesis) return
      window.speechSynthesis.cancel()
      const utter = new SpeechSynthesisUtterance(text.replace(/<[^>]+>/g, ''))
      utter.lang = 'zh-CN'
      utter.rate = 1.05
      utter.pitch = 1.1
      utter.onstart = () => { this.isSpeaking = true }
      utter.onend = () => { this.isSpeaking = false }
      utter.onerror = () => { this.isSpeaking = false }
      window.speechSynthesis.speak(utter)
    },
    goTo(path) {
      if (this.$route.path !== path) this.$router.push(path)
      this.visible = false
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const box = this.$refs.messageBox
        if (box) box.scrollTop = box.scrollHeight
      })
    },
    formatText(text) {
      return (text || '').replace(/\n/g, '<br>')
    },
    now() {
      const d = new Date()
      return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
    }
  }
}
</script>

<style lang="scss" scoped>
.digital-human {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 2000;
}

.dh-avatar-wrap {
  position: relative;
  cursor: pointer;
}

.dh-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #818cf8);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35);
  position: relative;
  transition: transform 0.3s;
  &:hover { transform: scale(1.08); }
}

.dh-face {
  width: 42px;
  height: 42px;
  background: rgba(255,255,255,0.95);
  border-radius: 50%;
  position: relative;
}

.dh-eyes {
  display: flex;
  justify-content: center;
  gap: 10px;
  padding-top: 14px;
}

.dh-eye {
  width: 6px;
  height: 6px;
  background: #4f46e5;
  border-radius: 50%;
  animation: dh-blink 3.5s infinite;
}

.dh-mouth {
  width: 14px;
  height: 6px;
  background: #4f46e5;
  border-radius: 0 0 14px 14px;
  margin: 8px auto 0;
  transition: all 0.2s;
  &.open {
    height: 10px;
    border-radius: 50%;
  }
}

.dh-ring {
  position: absolute;
  top: -6px; left: -6px; right: -6px; bottom: -6px;
  border: 2px solid rgba(99, 102, 241, 0.3);
  border-radius: 50%;
  animation: dh-pulse 2s infinite;
  &.delay { animation-delay: 1s; }
}

.dh-badge {
  position: absolute;
  top: -2px;
  right: -2px;
  min-width: 18px;
  height: 18px;
  line-height: 18px;
  text-align: center;
  background: #ef4444;
  color: #fff;
  border-radius: 9px;
  font-size: 11px;
  padding: 0 5px;
}

.dh-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.dh-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: linear-gradient(135deg, #4f46e5, #818cf8);
  color: #fff;
}

.dh-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dh-avatar-mini {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.dh-face-mini {
  width: 30px;
  height: 30px;
  background: #fff;
  border-radius: 50%;
  position: relative;
}

.dh-eyes-mini {
  display: flex;
  justify-content: center;
  gap: 6px;
  padding-top: 10px;
  div {
    width: 4px; height: 4px;
    background: #4f46e5;
    border-radius: 50%;
  }
}

.dh-mouth-mini {
  width: 10px;
  height: 4px;
  background: #4f46e5;
  border-radius: 0 0 10px 10px;
  margin: 5px auto 0;
}

.dh-name { font-size: 16px; font-weight: 700; }
.dh-status { font-size: 12px; opacity: 0.9; display: flex; align-items: center; gap: 4px; margin-top: 2px; }
.dh-dot { width: 6px; height: 6px; background: #4ade80; border-radius: 50%; }

.dh-header-actions {
  display: flex;
  gap: 14px;
}

.dh-action-icon {
  font-size: 18px;
  cursor: pointer;
  opacity: 0.9;
  transition: opacity 0.2s;
  &:hover { opacity: 1; }
}

.dh-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  background: #f8fafc;
}

.dh-message {
  margin-bottom: 16px;
  &.user { text-align: right; }
  &.assistant { text-align: left; }
}

.dh-bubble {
  display: inline-block;
  max-width: 86%;
  padding: 12px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  text-align: left;
}

.dh-message.user .dh-bubble {
  background: #4f46e5;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.dh-message.assistant .dh-bubble {
  background: #fff;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.03);
}

.dh-time {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 4px;
}

.dh-guide-title {
  font-weight: 700;
  color: #4f46e5;
  margin-bottom: 10px;
}

.dh-guide-steps {
  margin-bottom: 12px;
}

.dh-step {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
  align-items: flex-start;
}

.dh-step-num {
  width: 20px;
  height: 20px;
  line-height: 20px;
  text-align: center;
  background: #eef2ff;
  color: #4f46e5;
  border-radius: 50%;
  font-size: 12px;
  flex-shrink: 0;
}

.dh-step-text { color: #475569; font-size: 13px; }

.dh-quick-actions {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.dh-chips {
  padding: 10px 20px;
  background: #fff;
  border-top: 1px solid #f1f5f9;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.dh-chip {
  padding: 6px 12px;
  background: #eef2ff;
  color: #4f46e5;
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  &:hover { background: #4f46e5; color: #fff; }
}

.dh-input-area {
  padding: 12px 20px 20px;
  background: #fff;
  border-top: 1px solid #f1f5f9;
  display: flex;
  gap: 10px;
}

.dh-typing {
  display: flex;
  gap: 5px;
  align-items: center;
  padding: 14px;
  span {
    width: 7px; height: 7px;
    background: #cbd5e1;
    border-radius: 50%;
    animation: dh-typing 1s infinite;
    &:nth-child(2) { animation-delay: 0.2s; }
    &:nth-child(3) { animation-delay: 0.4s; }
  }
}

@keyframes dh-pulse {
  0% { transform: scale(1); opacity: 0.6; }
  100% { transform: scale(1.25); opacity: 0; }
}

@keyframes dh-blink {
  0%, 96%, 100% { transform: scaleY(1); }
  98% { transform: scaleY(0.1); }
}

@keyframes dh-typing {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

::v-deep .dh-drawer .el-drawer__header {
  display: none;
}

::v-deep .dh-drawer .el-drawer__body {
  padding: 0;
  overflow: hidden;
}
</style>
