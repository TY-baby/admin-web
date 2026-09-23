<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-form inline size="small">
        <el-form-item label="客户名称"><el-input v-model="query.keyword_name" placeholder="模糊搜索" clearable /></el-form-item>
        <el-form-item label="抖音ID"><el-input v-model="query.keyword_douyin" placeholder="模糊搜索" clearable /></el-form-item>
        <el-form-item label="添加时间">
          <el-date-picker v-model="dateRange" type="daterange" value-format="yyyy-MM-dd"
                          start-placeholder="开始" end-placeholder="结束" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load(1)">查询</el-button>
          <el-button icon="el-icon-refresh-left" @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading" row-key="id">
        <el-table-column type="expand">
          <template slot-scope="{ row }">
            <el-table :data="novelRows(row)" size="mini" border
                      :empty-text="'暂无网文投放记录'">
              <el-table-column prop="douyin_id" label="抖音ID" width="120" />
              <el-table-column label="推广链接" min-width="280">
                <template slot-scope="{ row: p }">
                  <a :href="p.link" target="_blank" style="color:#1f6bff">{{ p.link }}</a>
                </template>
              </el-table-column>
              <el-table-column prop="tier" label="档位" width="60" />
              <el-table-column prop="unit_price" label="单价" width="80" />
              <el-table-column prop="consumed" label="消耗" width="90" />
              <el-table-column prop="reads" label="实时阅读量" width="100" />
              <el-table-column prop="refresh_count" label="刷新次数" width="90" />
              <el-table-column label="投放时间" width="160">
                <template slot-scope="{ row: p }">{{ String(p.created_at).replace('T',' ').slice(0,19) }}</template>
              </el-table-column>
            </el-table>
          </template>
        </el-table-column>
        <el-table-column prop="customer_uid" label="客户UID" width="110" />
        <el-table-column prop="customer_name" label="客户名称" />
        <el-table-column prop="contact_name" label="联系人" width="100" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column label="投放链接数" width="100">
          <template slot-scope="{ row }">{{ novelRows(row).length }}</template>
        </el-table-column>
        <el-table-column label="总充值" width="100">
          <template slot-scope="{ row }">{{ (row.douyin_list||[]).reduce((s,a)=>s+Number(a.recharge_amount||0),0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="总剩余" width="100">
          <template slot-scope="{ row }">{{ (row.douyin_list||[]).reduce((s,a)=>s+Number(a.balance||0),0).toFixed(2) }}</template>
        </el-table-column>
        <el-table-column label="添加时间" width="160">
          <template slot-scope="{ row }">{{ String(row.created_at).replace('T',' ').slice(0,19) }}</template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" show-overflow-tooltip />
      </el-table>
      <el-pagination class="mt-16" background layout="total, sizes, prev, pager, next, jumper"
                     :total="total" :current-page="query.page" :page-size="query.page_size"
                     :page-sizes="[10,20,50,100]"
                     @current-change="p => load(p)"
                     @size-change="s => { query.page_size = s; load(1) }" />
    </el-card>
  </div>
</template>

<script>
import { listNovel } from '@/api/adminNovel'
export default {
  name: 'AdminNovel',
  data() {
    return {
      loading: false, rows: [], total: 0, dateRange: [],
      query: { keyword_name: '', keyword_douyin: '', page: 1, page_size: 20 }
    }
  },
  created() { this.load(1) },
  methods: {
    novelRows(row) {
      const out = []
      ;(row.douyin_list || []).forEach(a => {
        (a.novel_pages || []).forEach(p => out.push(Object.assign({ douyin_id: a.douyin_id }, p)))
      })
      return out
    },
    async load(page) {
      this.query.page = page || this.query.page
      const params = { ...this.query }
      if (this.dateRange && this.dateRange.length === 2) {
        params.date_from = this.dateRange[0]
        params.date_to = this.dateRange[1]
      }
      this.loading = true
      try {
        const { data } = await listNovel(params)
        if (data.code === 0) { this.rows = data.data.items; this.total = data.data.total }
      } finally { this.loading = false }
    },
    reset() {
      this.query = { keyword_name: '', keyword_douyin: '', page: 1, page_size: 20 }
      this.dateRange = []
      this.load(1)
    }
  }
}
</script>