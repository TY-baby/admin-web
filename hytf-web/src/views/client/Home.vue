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

    <div class="tabs">
      <div :class="['tab', tab==='novel'?'on':'']" @click="tab='novel'">网文推广</div>
      <div :class="['tab', tab==='live'?'on':'']" @click="tab='live'">直播</div>
    </div>

    <div class="main">
      <div class="left">
        <div class="card">
          <div class="card-title">我要投放的抖音号和商品</div>
          <el-select v-model="currentId" placeholder="请选择抖音号" style="width:100%" @change="onAccChange">
            <el-option v-for="a in accounts" :key="a.douyin_id"
                       :label="a.douyin_name + ' (' + a.douyin_id + ')'" :value="a.douyin_id" />
          </el-select>
        </div>

        <div class="card">
          <div class="card-title">申请流程</div>
          <video controls style="width:100%;border-radius:6px;background:#000" poster="">
            <source src="" type="video/mp4" />
            您的浏览器不支持视频播放
          </video>
        </div>

        <div class="card">
          <div class="card-title">日预算方案</div>
          <el-radio-group v-model="plan" size="medium">
            <el-radio-button label="A">A档300（一天）</el-radio-button>
            <el-radio-button label="B">B档600（一天）</el-radio-button>
            <el-radio-button label="C">C档1000（一天）</el-radio-button>
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
          <div class="money-row"><span class="lbl">抖音号数</span><span class="val">{{ summary.account_count || 0 }}</span></div>
        </div>

        <div class="card">
          <div class="card-title">新手常见问题</div>
          <ul class="faq">
            <li>1. 如何充值？请联系客服进行线下充值登记。</li>
            <li>2. 投放档位怎么选？根据充值金额系统自动匹配。</li>
            <li>3. 授权到期后怎么办？请联系客服续期。</li>
            <li>4. 数据多久更新一次？实时同步，可手动刷新。</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getSummary } from '@/api/clientHome'
export default {
  name: 'ClientHome',
  data() { return { tab: 'novel', plan: 'A', currentId: '', summary: {} } },
  computed: { ...mapState('clientUser', ['info', 'accounts', 'currentAccount']) },
  async created() {
    await this.$store.dispatch('clientUser/loadAccounts')
    if (this.accounts.length) this.currentId = this.accounts[0].douyin_id
    const { data } = await getSummary()
    if (data.code === 0) this.summary = data.data || {}
  },
  methods: {
    onAccChange(id) {
      const acc = this.accounts.find(a => a.douyin_id === id)
      this.$store.commit('clientUser/SET_CURRENT', acc)
      if (acc) this.plan = acc.tier
    },
    onLaunch() {
      this.$confirm('将使用【' + this.plan + '】档位方案进行投放，是否继续?', '一键投放', { type: 'info' })
        .then(() => { this.$router.push('/client/launch') }).catch(() => {})
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
  background: #fff; padding: 0 24px; border-bottom: 1px solid #ffe0ea; display: flex;
  .tab { padding: 12px 20px; cursor: pointer; color: #606266; font-size: 14px;
    border-bottom: 2px solid transparent;
    &.on { color: #ff2e63; border-bottom-color: #ff2e63; font-weight: bold; } }
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
.money-row {
  display: flex; justify-content: space-between; padding: 6px 0; font-size: 13px;
  .lbl { color: #909399; } .val { color: #ff2e63; font-weight: bold; }
}
.faq { padding-left: 18px; margin: 0; color: #606266; font-size: 13px; line-height: 1.9; }
</style>