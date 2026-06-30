<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">通讯录</div>
      <div class="oa-desc">员工联系方式、部门通讯录与企业内联</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-input v-model="keyword" placeholder="姓名/手机号/部门" clearable style="width:260px" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-download">导出通讯录</el-button>
      </div>
      <el-table :data="list" border v-loading="loading">
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="dept" label="部门" width="120" />
        <el-table-column prop="position" label="职位" width="140" />
        <el-table-column prop="phone" label="手机号" width="140" />
        <el-table-column prop="email" label="企业邮箱" />
        <el-table-column label="操作" width="160">
          <template>
            <el-button type="text">详情</el-button>
            <el-button type="text">发消息</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination class="oa-pagination" background layout="prev, pager, next" :total="86" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      keyword: '',
      list: [
        { name: '张伟', dept: '研发部', position: '高级工程师', phone: '13800138001', email: 'zhangwei@base-room.com' },
        { name: '李娜', dept: '财务部', position: '财务主管', phone: '13800138002', email: 'lina@base-room.com' },
        { name: '王强', dept: '生产部', position: '车间主任', phone: '13800138003', email: 'wangqiang@base-room.com' },
        { name: '赵敏', dept: '采购部', position: '采购经理', phone: '13800138004', email: 'zhaomin@base-room.com' }
      ]
    }
  },
  methods: {
    load() {
      this.loading = true
      setTimeout(() => { this.loading = false }, 300)
    }
  }
}
</script>

<style lang="scss" scoped>
.oa-page { padding: 20px; }
.oa-header {
  background: linear-gradient(135deg, #f97316, #fb923c);
  border-radius: 12px;
  padding: 24px;
  color: #fff;
  margin-bottom: 20px;
}
.oa-title { font-size: 22px; font-weight: 700; margin-bottom: 6px; }
.oa-desc { font-size: 14px; opacity: 0.9; }
.oa-card {
  background: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.oa-toolbar { display: flex; gap: 12px; margin-bottom: 16px; }
.oa-pagination { margin-top: 16px; text-align: right; }
</style>
