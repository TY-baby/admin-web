<template>
  <div class="oa-page">
    <div class="oa-header">
      <div class="oa-title">组织架构</div>
      <div class="oa-desc">部门管理、岗位设置与人员编制</div>
    </div>

    <div class="oa-card">
      <div class="oa-toolbar">
        <el-input v-model="keyword" placeholder="部门名称" clearable style="width:260px" />
        <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
        <el-button type="success" icon="el-icon-plus">新增部门</el-button>
      </div>
      <el-tree :data="depts" :props="{ label: 'name', children: 'children' }" default-expand-all>
        <span slot-scope="{ node, data }">
          <span><i :class="data.icon || 'el-icon-office-building'" style="margin-right:6px;color:#3b82f6"></i>{{ node.label }}</span>
          <span style="margin-left:20px;color:#94a3b8;font-size:12px">{{ data.count }} 人</span>
        </span>
      </el-tree>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      keyword: '',
      depts: [
        {
          name: 'Base Room 科技有限公司',
          count: 86,
          icon: 'el-icon-s-home',
          children: [
            { name: '总经办', count: 3, icon: 'el-icon-s-custom' },
            { name: '研发部', count: 28, icon: 'el-icon-s-platform' },
            { name: '产品部', count: 8, icon: 'el-icon-s-opportunity' },
            { name: '销售部', count: 18, icon: 'el-icon-s-shop' },
            { name: '市场部', count: 6, icon: 'el-icon-s-marketing' },
            { name: '生产部', count: 12, icon: 'el-icon-s-tools' },
            { name: '财务部', count: 5, icon: 'el-icon-s-finance' },
            { name: '人事行政部', count: 6, icon: 'el-icon-s-check' }
          ]
        }
      ]
    }
  },
  methods: {
    load() {
      this.$message.success('组织架构已刷新')
    }
  }
}
</script>

<style lang="scss" scoped>
.oa-page { padding: 20px; }
.oa-header {
  background: linear-gradient(135deg, #10b981, #34d399);
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
</style>
