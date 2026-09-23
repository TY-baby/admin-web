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
        <div :class="['tab', tab==='live'?'on':'']" @click="tab='live'">
          <i class="el-icon-video-camera tab-ico"></i>直播
        </div>
        <div :class="['tab', tab==='novel'?'on':'']" @click="tab='novel'">
          <i class="el-icon-reading tab-ico"></i>网文推广
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
          <div class="card-title">{{ tab === 'live' ? '我要投放的抖音号和商品' : '我要投放的ID' }}</div>
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
          <div class="card-title">{{ tab === 'live' ? '日结算方案' : '日预算方案' }}</div>
          <el-radio-group v-model="plan" size="medium">
            <template v-if="tab === 'live'">
              <el-radio-button label="A">A档300/条</el-radio-button>
              <el-radio-button label="B">B档600/条</el-radio-button>
              <el-radio-button label="C">C档1000/条</el-radio-button>
            </template>
            <template v-else>
              <el-radio-button label="A">A档998/条（1h内）</el-radio-button>
              <el-radio-button label="B">B档1998/条（1h内）</el-radio-button>
              <el-radio-button label="C">C档3998/条（1h内）</el-radio-button>
            </template>
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
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getSummary, launchDelivery, launchNovel } from '@/api/clientHome'
export default {
  name: 'ClientHome',
  data() { return { tab: 'live', plan: 'A', currentId: '', summary: {} } },
  computed: { ...mapState('clientUser', ['info', 'accounts', 'currentAccount']) },
  async created() {
    await this.$store.dispatch('clientUser/loadAccounts')
    if (this.accounts.length) {
      this.currentId = this.accounts[0].douyin_id
      if (this.accounts[0].tier) this.plan = this.accounts[0].tier
    }
    const { data } = await getSummary()
    if (data.code === 0) this.summary = data.data || {}
  },
  methods: {
    onAccChange(id) {
      const acc = this.accounts.find(a => a.douyin_id === id)
      this.$store.commit('clientUser/SET_CURRENT', acc)
      if (acc && acc.tier) this.plan = acc.tier
    },
    onLaunch() {
      if (!this.currentId) { this.$message.warning('请先选择抖音号'); return }
      const acc = this.accounts.find(a => a.douyin_id === this.currentId)
      const isNovel = this.tab === 'novel'
      const price = isNovel ? { A: 998, B: 1998, C: 3998 }[this.plan]
                            : { A: 300, B: 600, C: 1000 }[this.plan]
      if (acc && acc.balance < price) { this.$message.error('账号余额不足,请联系管理员充值'); return }
      this.$confirm('将使用【' + this.plan + '】档位方案进行投放,并记录档位与投放时间,是否继续?', '一键投放', { type: 'info' })
        .then(async () => {
          const api = isNovel ? launchNovel : launchDelivery
          const { data } = await api({ douyin_id: this.currentId, tier: this.plan })
          if (data.code === 0) {
            const d = data.data || {}
            if (isNovel) {
              this.$alert('本次消耗' + d.consumed + '元,剩余流水' + d.remaining + '元<br/>推广链接：<a href="' + d.link + '" target="_blank">' + d.link + '</a>',
                          '投放成功', { dangerouslyUseHTMLString: true, type: 'success' })
            } else {
              this.$message.success('投放成功,本次消耗' + d.consumed + '元,剩余流水' + d.remaining + '元')
              this.$router.push('/client/launch')
            }
            await this.$store.dispatch('clientUser/loadAccounts')
          } else {
            this.$message.error(data.msg || '投放失败')
          }
        }).catch(() => {})
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
// 文件夹式 tab（位于 banner 底部，与下方面板衔接）
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
      // 右侧斜切边：上窄下宽，模拟参考站文件夹 tab
      &::after {
        content: ''; position: absolute; top: 0; left: 100%; width: 22px; height: 100%;
        background: #fdeff4; clip-path: polygon(0 0, 0 100%, 100% 100%);
      }
    }
  }
  .tabs-tip { margin-left: auto; align-self: center; padding-right: 20px; font-size: 13px; color: #8f8f96; }
}
// 顶部促销 banner（居中展示，引流感）
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
// 内容居中容器
.main-wrap { max-width: 1200px; margin: 0 auto; }
// tab 下方浅粉面板，与选中 tab 背景色衔接
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
.money-row {
  display: flex; justify-content: space-between; padding: 6px 0; font-size: 13px;
  .lbl { color: #909399; } .val { color: #ff2e63; font-weight: bold; }
}
.faq { padding-left: 18px; margin: 0; color: #606266; font-size: 13px; line-height: 1.9; }
</style>