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
          <div slot="header">杩?14 澶╄祫閲戞祦姘磋秼鍔?/div>
          <line-chart :dates="dates" :series="series" height="340px" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <div slot="header">杩愯惀棰勮</div>
          <div class="alert-item"><span>鍗冲皢鍒版湡鎶栭煶鍙?/span><b style="color:#E6A23C">{{ data.expiring_count || 0 }}</b></div>
          <div class="alert-item"><span>宸插埌鏈熸姈闊冲彿</span><b style="color:#F56C6C">{{ data.expired_count || 0 }}</b></div>
          <div class="alert-item"><span>寰呭紑绁ㄨ褰?/span><b style="color:#409EFF">{{ data.invoice_pending || 0 }}</b></div>
          <el-divider />
          <div class="text-muted" style="font-size:12px;line-height:1.7">
            鏈嶅姟鍣ㄩ璀﹂槇鍊?2鏍?G)锛?br />
            CPU &gt; 80% / 鍐呭瓨 &gt; 80% / QPS &gt; 200<br />
            瑙﹀彂鏃跺悗绔棩蹇椾細杈撳嚭 WARN 璁板綍
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
        { key: 'c', title: '瀹㈡埛鎬绘暟', value: d.total_customer || 0 },
        { key: 'd', title: '鎶栭煶鍙锋€绘暟', value: d.total_douyin || 0 },
        { key: 'r', title: '绱鍏呭€?鍏?', value: Number(d.total_recharge || 0).toFixed(2) },
        { key: 'x', title: '绱娑堣€?鍏?', value: Number(d.total_consume || 0).toFixed(2) }
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
        { name: '鍏呭€?, data: t.map(x => x.recharge), color: '#67C23A' },
        { name: '娑堣€?, data: t.map(x => x.consume), color: '#F56C6C' },
        { name: '浣欓', data: t.map(x => x.balance), color: '#409EFF' }
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