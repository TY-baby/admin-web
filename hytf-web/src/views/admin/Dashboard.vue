<template>
  <div>
    <el-row :gutter="16" class="mb-16">
      <el-col :span="6" v-for="c in cards" :key="c.key">
        <el-card shadow="hover">
          <div class="text-muted">{{ c.title }}</div>
          <div class="big">{{ c.value }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="16">
      <el-col :span="16">
        <el-card shadow="never">
          <div slot="header">近 14 天资金流水趋势</div>
          <line-chart :dates="dates" :series="series" height="340px" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <div slot="header">运营预警</div>
          <div class="alert-item"><span>即将到期抖音号</span><b style="color:#E6A23C">{{ data.expiring_count || 0 }}</b></div>
          <div class="alert-item"><span>已到期抖音号</span><b style="color:#F56C6C">{{ data.expired_count || 0 }}</b></div>
          <div class="alert-item"><span>待开票记录</span><b style="color:#409EFF">{{ data.invoice_pending || 0 }}</b></div>
          <el-divider />
          <div class="text-muted" style="font-size:12px;line-height:1.7">
            服务器预警阈值(2核8G)。<br />
            CPU &gt; 80% / 内存 &gt; 80% / QPS &gt; 200<br />
            触发时后端日志会输出 WARN 记录
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getOverview } from '@/api/adminDashboard'
import LineChart from '@/components/LineChart.vue'
export default {
  name: 'AdminDashboard',
  components: { LineChart },
  data() { return { data: {}, dates: [], series: [] } },
  computed: {
    cards() {
      const d = this.data || {}
      return [
        { key: 'c', title: '客户总数', value: d.total_customer || 0 },
        { key: 'd', title: '抖音号总数', value: d.total_douyin || 0 },
        { key: 'r', title: '累计充值(元)', value: Number(d.total_recharge || 0).toFixed(2) },
        { key: 'x', title: '累计消费(元)', value: Number(d.total_consume || 0).toFixed(2) }
      ]
    }
  },
  async created() {
    const { data } = await getOverview({ days: 14 })
    if (data.code === 0) {
      this.data = data.data
      const t = data.data.trend || []
      this.dates = t.map(x => x.date)
      this.series = [
        { name: '充值', data: t.map(x => x.recharge), color: '#67C23A' },
        { name: '消费', data: t.map(x => x.consume), color: '#F56C6C' },
        { name: '余额', data: t.map(x => x.balance), color: '#409EFF' }
      ]
    }
  }
}
</script>

<style scoped>
.big { font-size: 24px; font-weight: bold; margin-top: 6px; color: #303133; }
.alert-item {
  display: flex; justify-content: space-between;
  padding: 10px 0; border-bottom: 1px dashed #eee;
  font-size: 14px;
}
</style>