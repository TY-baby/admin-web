<template>
  <div>
    <el-page-header @back='() => $router.back()' content='客户详情' />
    <el-card style='margin-top: 20px;' v-if='customer'>
      <div slot='header'><span>{{ customer.name }}</span></div>
      <el-descriptions :column='3' border>
        <el-descriptions-item label='电话'>{{ customer.phone }}</el-descriptions-item>
        <el-descriptions-item label='公司'>{{ customer.company }}</el-descriptions-item>
        <el-descriptions-item label='行业'>{{ customer.industry }}</el-descriptions-item>
        <el-descriptions-item label='来源'>{{ customer.source }}</el-descriptions-item>
        <el-descriptions-item label='状态'>{{ customer.status }}</el-descriptions-item>
        <el-descriptions-item label='等级'>{{ customer.level }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
    <el-row :gutter='20' style='margin-top: 20px;'>
      <el-col :span='12'>
        <el-card>
          <div slot='header'>联系人</div>
          <el-table :data='customer.contacts || []' size='small'>
            <el-table-column prop='name' label='姓名' />
            <el-table-column prop='phone' label='电话' />
            <el-table-column prop='position' label='职位' />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span='12'>
        <el-card>
          <div slot='header'>跟进记录</div>
          <el-timeline>
            <el-timeline-item v-for='f in customer.follows || []' :key='f.id' :timestamp='f.create_time'>{{ f.content }}</el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getCustomerDetail } from '@/api/customer'
export default {
  data() { return { customer: {} } },
  created() { this.load() },
  methods: { async load() { this.customer = await getCustomerDetail(this.$route.params.id) } }
}
</script>
