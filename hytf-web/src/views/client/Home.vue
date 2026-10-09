<template>
  <div class="client-layout">
    <div class="topbar flex-between">
      <div class="logo">恒耀互娱</div>
      <div class="nav">
        <router-link to="/client/home" class="nav-item active">首页</router-link>
        <router-link to="/client/finance" class="nav-item">财务</router-link>
      </div>
      <div class="user">
        <span>{{ info.customer_name || info.phone }}</span>
        <el-button type="text" @click="logout">退出</el-button>
      </div>
    </div>

    <div class="banner">
      <div class="banner-inner">
        <span class="bn-txt">新客限时</span>
        <span class="bn-arrow">↗</span>
        <span class="bn-txt">专享投放</span>
      </div>
      <div class="tabs">
        <div :class="['tab', tab==='first'?'on':'']" @click="switchTab('first')">
          <i class="el-icon-video-camera tab-ico"></i>首充
        </div>
        <div :class="['tab', tab==='exposure'?'on':'']" @click="switchTab('exposure')">
          <i class="el-icon-data-line tab-ico"></i>直播曝光度
        </div>
        <div class="tabs-tip">想要进行更多自定义投放？请联系客服咨询</div>
      </div>
    </div>

    <div class="main-wrap">
      <div class="panel">
        <div class="panel-head">为您优选专属投放方案</div>
        <div class="main">
          <div class="left">
            <div class="card">
              <div class="card-title">投放平台</div>
              <el-select v-model="platform" placeholder="请选择投放平台" style="width:100%" @change="onPlatformChange">
                <el-option v-for="p in platforms" :key="p.code" :label="p.name" :value="p.code" />
              </el-select>
            </div>

            <div class="card">
              <div class="card-title">我要投放的ID</div>
              <el-select v-model="currentId" :placeholder="platform ? '请选择' + platformName + 'ID' : '请先选择投放平台'"
                         :disabled="!platform" style="width:100%" @change="onAccChange">
                <el-option v-for="a in platformAccounts" :key="a.id"
                           :label="a.douyin_id + (a.douyin_name ? '（' + a.douyin_name + '）' : '')"
                           :value="a.douyin_id" />
              </el-select>
            </div>

            <div class="card">
              <div class="card-title">日预算</div>
              <el-input v-model="dailyBudget" placeholder="请输入日预算,单位元" style="width:100%">
                <template slot="append">元</template>
              </el-input>
              <div v-if="budgetError" class="budget-err">{{ budgetError }}</div>
            </div>

            <div class="card">
              <div class="card-title">申请流程</div>
              <video controls preload="metadata" playsinline src="/media/promo.mp4"
                     style="width:100%;border-radius:6px;background:#000">
                您的浏览器不支持视频播放
              </video>
            </div>

            <div class="card">
              <div class="card-title">{{ tab === 'first' ? '日结算方案' : '曝光度方案（1h内曝光）' }}</div>
              <el-radio-group v-model="plan" class="tier-vertical">
                <el-radio v-for="t in tierOptions" :key="t.value" :label="t.value" class="tier-item">{{ t.label }}</el-radio>
              </el-radio-group>
              <div style="margin-top:16px">
                <el-button type="primary" size="medium" class="hy-cta" icon="el-icon-s-promotion" @click="onLaunch">一键投放</el-button>
              </div>
            </div>
          </div>

          <div class="right">
            <div class="card">
              <div class="card-title">我的资金</div>
              <div class="money-row"><span class="lbl">账户余额</span><span class="val">￥{{ summary.total_balance || 0 }}</span></div>
              <div class="money-row"><span class="lbl">累计充值</span><span class="val">￥{{ summary.total_recharge || 0 }}</span></div>
              <div class="money-row"><span class="lbl">累计消费</span><span class="val">￥{{ summary.total_consume || 0 }}</span></div>
              <div class="money-row"><span class="lbl">投放ID数</span><span class="val">{{ summary.account_count || 0 }}</span></div>
            </div>

            <div class="card">
              <div class="card-title">新手常见问题</div>
              <ul class="faq">
                <li>1. 如何充值？请联系客服进行线下充值登记。</li>
                <li>2. 投放档位怎么选？根据日预算与档位金额计算生成条数。</li>
                <li>3. 授权到期后怎么办？请联系客服续期。</li>
                <li>4. 数据什么时候能查？投放成功次日起可查询。</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="progressVisible" class="launch-mask">
      <div class="launch-box">
        <div class="launch-title">正在提交投放,请稍候...</div>
        <el-progress :percentage="progress" :stroke-width="14" color="#ff2e63" />
      </div>
    </div>

    <el-dialog :visible.sync="confirmVisible" width="420px" custom-class="launch-confirm"
               :close-on-click-modal="false" append-to-body>
      <div slot="title" class="lc-head">
        <i class="el-icon-s-promotion"></i><span>确认投放信息</span>
      </div>
      <div class="lc-body">
        <div class="lc-row"><span class="k">投放平台</span><span class="v">{{ confirmInfo.platformName }}</span></div>
        <div class="lc-row"><span class="k">投放ID</span><span class="v">{{ confirmInfo.id }}</span></div>
        <div class="lc-row"><span class="k">投放类型</span><span class="v"><em class="tag">{{ confirmInfo.typeLabel }}</em></span></div>
        <div class="lc-row"><span class="k">所选档位</span><span class="v">{{ confirmInfo.tier }} 档（{{ confirmInfo.price }} 元）</span></div>
        <div class="lc-row"><span class="k">日预算</span><span class="v hl">￥{{ confirmInfo.budget }}</span></div>
        <div class="lc-row"><span class="k">预计生成</span><span class="v hl">{{ confirmInfo.generated }} 条</span></div>
      </div>
      <div slot="footer">
        <el-button size="small" @click="confirmVisible=false">再想想</el-button>
        <el-button size="small" type="danger" @click="doConfirmLaunch">确认投放</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getSummary, launchDelivery, launchNovel, getPlatforms } from '@/api/clientHome'

const FIRST_TIERS = [
  { value: 'A', label: 'A档 300/条', price: 300 },
  { value: 'B', label: 'B档 600/条', price: 600 },
  { value: 'C', label: 'C档 1000/条', price: 1000 }
]
const EXPOSURE_TIERS = [
  { value: 'A', label: 'A档 1998（1h内曝光）', price: 1998 },
  { value: 'B', label: 'B档 2998（1h内曝光）', price: 2998 },
  { value: 'C', label: 'C档 5998（1h内曝光）', price: 5998 }
]

export default {
  name: 'ClientHome',
  data() {
    return {
      tab: 'first', platform: '', currentId: '', plan: '',
      dailyBudget: '', summary: {}, platforms: [],
      progressVisible: false, progress: 0, launching: false,
      confirmVisible: false, confirmInfo: {}, pendingLaunch: null
    }
  },
  computed: {
    ...mapState('clientUser', ['info', 'accounts', 'currentAccount']),
    tierOptions() { return this.tab === 'first' ? FIRST_TIERS : EXPOSURE_TIERS },
    platformName() {
      const p = this.platforms.find(x => x.code === this.platform)
      return p ? p.name : ''
    },
    platformAccounts() {
      return (this.accounts || []).filter(a => a.platform_code === this.platform)
    },
    selectedAccount() {
      return (this.accounts || []).find(a => a.platform_code === this.platform && a.douyin_id === this.currentId)
    },
    budgetError() {
      if (this.dailyBudget === '' || this.dailyBudget === null) return ''
      const v = Number(this.dailyBudget)
      if (isNaN(v) || v <= 0) return '请输入大于0的数字'
      if (this.selectedAccount && v > Number(this.selectedAccount.balance)) {
        return '日预算不能超过当前账号余额（￥' + Number(this.selectedAccount.balance).toFixed(2) + '）'
      }
      return ''
    }
  },
  async created() {
    const [{ data: pd }] = await Promise.all([
      getPlatforms(),
      this.$store.dispatch('clientUser/loadAccounts')
    ])
    if (pd.code === 0) this.platforms = pd.data || []
    const { data } = await getSummary()
    if (data.code === 0) this.summary = data.data || {}
  },
  methods: {
    switchTab(t) { this.tab = t; this.plan = '' },
    onPlatformChange() { this.currentId = '' },
    onAccChange(id) {
      const acc = this.platformAccounts.find(a => a.douyin_id === id)
      this.$store.commit('clientUser/SET_CURRENT', acc)
    },
    validateLaunch() {
      if (!this.platform) { this.$message.warning('请选择投放平台'); return false }
      if (!this.currentId) { this.$message.warning('请选择要投放的ID'); return false }
      if (!this.plan) { this.$message.warning('请选择档位方案'); return false }
      const budget = Number(this.dailyBudget)
      if (this.dailyBudget === '' || isNaN(budget) || budget <= 0) {
        this.$message.warning('请输入日预算'); return false
      }
      const acc = this.selectedAccount
      if (acc && budget > Number(acc.balance)) {
        this.$message.error('日预算不能超过当前账号余额'); return false
      }
      const tier = this.tierOptions.find(t => t.value === this.plan)
      if (tier && budget < tier.price) {
        this.$message.error('日预算不能小于所选档位金额（' + tier.price + '元）'); return false
      }
      return true
    },
    onLaunch() {
      if (!this.validateLaunch()) return
      const tier = this.tierOptions.find(t => t.value === this.plan)
      const generated = Math.floor(Number(this.dailyBudget) / tier.price)
      const typeLabel = this.tab === 'first' ? '首充' : '直播曝光度'
      this.confirmInfo = {
        platformName: this.platformName, id: this.currentId, typeLabel,
        tier: this.plan, price: tier.price, budget: this.dailyBudget, generated
      }
      this.pendingLaunch = { tier, typeLabel, generated }
      this.confirmVisible = true
    },
    doConfirmLaunch() {
      this.confirmVisible = false
      if (this.pendingLaunch) {
        const { tier, typeLabel, generated } = this.pendingLaunch
        this.doLaunch(tier, typeLabel, generated)
      }
    },
    async doLaunch(tier, typeLabel, generated) {
      if (this.launching) return
      this.launching = true
      this.progressVisible = true
      this.progress = 0
      const payload = {
        platform_code: this.platform,
        douyin_id: this.currentId,
        tier: this.plan,
        daily_budget: Number(this.dailyBudget)
      }
      const api = this.tab === 'first' ? launchDelivery : launchNovel
      let result = null
      try {
        const { data } = await api(payload)
        result = data
      } catch (e) {
        result = { code: -1, msg: (e && e.message) || '网络异常' }
      }
      // 进度条 5 秒走到 100%，再根据结果跳转或提示
      const timer = setInterval(() => {
        this.progress = Math.min(100, this.progress + 2)
        if (this.progress >= 100) {
          clearInterval(timer)
          this.progressVisible = false
          this.launching = false
          if (result && result.code === 0) {
            this.$message({ type: 'success', duration: 5000,
              message: '投放成功（' + typeLabel + ' ' + generated + ' 条），数据需等待一个工作日后方可查询' })
            this.$store.dispatch('clientUser/loadAccounts')
            this.$router.push('/client/launch')
          } else {
            this.$message.error((result && result.msg) || '投放失败')
          }
        }
      }, 100)
    },
    logout() {
      this.$store.dispatch('clientUser/logout')
      this.$router.push('/client/login')
    }
  }
}
</script>

<style scoped lang="scss">
.client-layout { min-height: 100vh; background: linear-gradient(160deg, #fff0f5 0%, #ffe8ef 45%, #ffeef4 100%); }
.topbar {
  height: 56px; padding: 0 24px;
  background: linear-gradient(135deg, #ff5f8f 0%, #ff2e63 100%);
  box-shadow: 0 2px 12px rgba(255, 46, 99, .25);
  .logo { font-weight: bold; font-size: 18px; color: #fff; }
  .nav-item { margin: 0 12px; color: rgba(255,255,255,.85); font-size: 14px;
    &.active { color: #fff; font-weight: bold; border-bottom: 2px solid #fff; } }
  .user span { margin-right: 8px; color: rgba(255,255,255,.9); font-size: 13px; }
  ::v-deep .el-button--text { color: #fff; }
}
.tabs {
  max-width: 1200px; margin: 26px auto 0; display: flex; align-items: stretch;
  background: rgba(255, 255, 255, .35); border-radius: 10px 10px 0 0;
  .tab {
    position: relative; display: flex; align-items: center; gap: 8px;
    padding: 14px 30px; font-size: 15px; font-weight: bold; color: #8f8f96; cursor: pointer;
    .tab-ico { font-size: 18px; color: #a5a5ad; }
    &:hover { color: #ff2e63; .tab-ico { color: #ff2e63; } }
    &.on {
      z-index: 1; background: #fdeff4; color: #303133; border-top-left-radius: 10px;
      .tab-ico { color: #ff2e63; }
      &::after {
        content: ''; position: absolute; top: 0; left: 100%; width: 22px; height: 100%;
        background: #fdeff4; clip-path: polygon(0 0, 0 100%, 100% 100%);
      }
    }
  }
  .tabs-tip { margin-left: auto; align-self: center; padding-right: 20px; font-size: 13px; color: #8f8f96; }
}
.banner {
  background: linear-gradient(120deg, #ff5f8f 0%, #ff2e63 50%, #ff7eb3 100%);
  padding: 30px 0 0; overflow: hidden;
}
.banner-inner {
  max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: center; gap: 28px;
}
.bn-txt {
  color: #fff; font-size: 34px; font-weight: 800; letter-spacing: 6px;
  text-shadow: 0 4px 16px rgba(0,0,0,.18);
}
.bn-arrow {
  color: #ffd7e4; font-size: 44px; font-weight: 800; line-height: 1;
  transform: rotate(0deg); text-shadow: 0 4px 16px rgba(0,0,0,.2);
}
.main-wrap { max-width: 1200px; margin: 0 auto; }
.panel {
  background: #fdeff4; border-radius: 0 0 12px 12px;
  .panel-head { padding: 22px 20px 0; font-size: 17px; font-weight: bold; color: #303133; }
}
.main {
  display: flex; padding: 16px; gap: 16px;
  .left { flex: 2; display: flex; flex-direction: column; gap: 16px; }
  .right { flex: 1; display: flex; flex-direction: column; gap: 16px; }
}
.card {
  background: #fff; border-radius: 12px; padding: 18px;
  box-shadow: 0 4px 16px rgba(255, 46, 99, .08);
  .card-title { font-size: 15px; font-weight: bold; color: #303133; margin-bottom: 12px;
    border-left: 3px solid #ff2e63; padding-left: 8px; }
}
.budget-err { color: #f56c6c; font-size: 12px; margin-top: 6px; line-height: 1.5; }
.tier-vertical {
  display: flex; flex-direction: column; align-items: flex-start; gap: 10px;
  .tier-item { margin-right: 0; padding: 10px 16px; width: 100%;
    border: 1px solid #ffd7e4; border-radius: 8px;
    ::v-deep .el-radio__label { font-size: 14px; }
    &:hover { border-color: #ff2e63; }
  }
  ::v-deep .el-radio.is-checked { .el-radio__label { color: #ff2e63; font-weight: bold; } }
}
.launch-mask {
  position: fixed; inset: 0; background: rgba(0, 0, 0, .55);
  display: flex; align-items: center; justify-content: center; z-index: 3000;
  .launch-box {
    width: 420px; background: #fff; border-radius: 12px; padding: 32px 28px;
    .launch-title { font-size: 15px; font-weight: bold; color: #303133; margin-bottom: 20px; text-align: center; }
  }
}
.money-row {
  display: flex; justify-content: space-between; padding: 6px 0; font-size: 13px;
  .lbl { color: #909399; } .val { color: #ff2e63; font-weight: bold; }
}
.faq { padding-left: 18px; margin: 0; color: #606266; font-size: 13px; line-height: 1.9; }
::v-deep .launch-confirm {
  border-radius: 14px; overflow: hidden;
  .el-dialog__header { background: linear-gradient(135deg, #ff5f8f, #ff2e63); padding: 16px 20px; }
  .el-dialog__headerbtn .el-dialog__close { color: #fff; }
  .el-dialog__body { padding: 20px 24px 8px; }
  .el-dialog__footer { padding: 12px 24px 20px; }
}
.lc-head { color: #fff; font-size: 16px; font-weight: bold; display: flex; align-items: center; gap: 8px; }
.lc-body { .lc-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 11px 4px; border-bottom: 1px dashed #ffe0ea; font-size: 14px;
    &:last-child { border-bottom: none; }
    .k { color: #909399; }
    .v { color: #303133; font-weight: 600; }
    .v.hl { color: #ff2e63; font-size: 16px; font-weight: bold; }
    .tag { font-style: normal; background: #fff0f5; color: #ff2e63; padding: 2px 10px; border-radius: 10px; font-size: 12px; }
  } }
</style>