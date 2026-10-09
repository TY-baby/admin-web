<template>
  <div>
    <el-card shadow="never" class="mb-16">
      <el-button type="primary" icon="el-icon-plus" size="small" @click="openAdd">新增普通用户</el-button>
      <span class="text-muted" style="margin-left:12px;font-size:12px">普通用户登录后仅可见被勾选的菜单</span>
    </el-card>
    <el-card shadow="never">
      <el-table :data="rows" border stripe v-loading="loading">
        <el-table-column prop="username" label="账号" width="130" />
        <el-table-column prop="real_name" label="姓名" width="120" />
        <el-table-column label="角色" width="100">
          <template slot-scope="{ row }">
            <el-tag size="mini" :type="row.role === 'user' ? 'info' : 'danger'">{{ row.role === 'user' ? '普通用户' : '超级' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="可见菜单">
          <template slot-scope="{ row }">{{ menuText(row) }}</template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template slot-scope="{ row }">
            <el-tag size="mini" :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '启用' : '停用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="最近登录" width="170">
          <template slot-scope="{ row }">{{ row.last_login_at ? String(row.last_login_at).replace('T',' ').slice(0,19) : '-' }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template slot-scope="{ row }">
            <el-button size="mini" type="text" @click="openEdit(row)">编辑</el-button>
            <el-button size="mini" type="text"
                       :style="{ color: row.is_active ? '#E6A23C' : '#67C23A' }"
                       @click="toggleActive(row)">{{ row.is_active ? '停用' : '启用' }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="form.id ? '编辑账号' : '新增普通用户'" :visible.sync="visible"
               width="520px" :close-on-click-modal="false">
      <el-form ref="aform" :model="form" :rules="rules" label-width="90px" size="small">
        <el-form-item label="账号" prop="username">
          <el-input v-model="form.username" :disabled="!!form.id" maxlength="50" placeholder="登录账号" />
        </el-form-item>
        <el-form-item label="密码" :prop="form.id ? '' : 'password'">
          <el-input v-model="form.password" type="password" show-password
                    :placeholder="form.id ? '留空则不修改密码' : '至少6位'" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.real_name" maxlength="50" placeholder="真实姓名（可选）" />
        </el-form-item>
        <el-form-item label="可见菜单">
          <el-checkbox-group v-model="form.menus">
            <el-checkbox v-for="m in menuOptions" :key="m.key" :label="m.key">{{ m.title }}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button size="small" @click="visible=false">取消</el-button>
        <el-button size="small" type="primary" :loading="saving" @click="submit">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { listAccounts, createAccount, updateAccount } from '@/api/adminSystem'

const MENU_LABELS = {
  dashboard: '首页', customer: '用户管理', novel: '网文客户', invoice: '开票管理',
  withdraw: '出款管理', log: '日志记录', monitor: '服务器监控', account: '账号管理'
}

export default {
  name: 'AdminAccount',
  data() {
    return {
      loading: false, saving: false, visible: false, rows: [],
      menuOptions: [
        { key: 'dashboard', title: '首页' },
        { key: 'customer', title: '用户管理' },
        { key: 'novel', title: '网文客户' },
        { key: 'invoice', title: '开票管理' },
        { key: 'withdraw', title: '出款管理' }
      ],
      form: { id: null, username: '', password: '', real_name: '', menus: [] },
      rules: {
        username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码至少6位', trigger: 'blur' }]
      }
    }
  },
  created() { this.load() },
  methods: {
    menuText(row) {
      if (row.role === 'super' || row.role === 'admin') return '全部菜单'
      const keys = (row.menus || '').split(',').filter(x => x)
      return keys.length ? keys.map(k => MENU_LABELS[k] || k).join('、') : '（无）'
    },
    async load() {
      this.loading = true
      try {
        const { data } = await listAccounts()
        if (data.code === 0) this.rows = data.data || []
      } finally { this.loading = false }
    },
    openAdd() {
      this.form = { id: null, username: '', password: '', real_name: '', menus: ['dashboard'] }
      this.visible = true
      this.$nextTick(() => this.$refs.aform && this.$refs.aform.clearValidate())
    },
    openEdit(row) {
      this.form = {
        id: row.id, username: row.username, password: '', real_name: row.real_name,
        menus: (row.menus || '').split(',').filter(x => x)
      }
      this.visible = true
      this.$nextTick(() => this.$refs.aform && this.$refs.aform.clearValidate())
    },
    submit() {
      this.$refs.aform.validate(async ok => {
        if (!ok) return
        this.saving = true
        try {
          const payload = { real_name: this.form.real_name, menus: this.form.menus }
          let res
          if (this.form.id) {
            if (this.form.password) payload.password = this.form.password
            res = await updateAccount(this.form.id, payload)
          } else {
            payload.username = this.form.username
            payload.password = this.form.password
            payload.role = 'user'
            res = await createAccount(payload)
          }
          if (res.data.code === 0) { this.$message.success('已保存'); this.visible = false; this.load() }
          else this.$message.error(res.data.msg || '保存失败')
        } finally { this.saving = false }
      })
    },
    toggleActive(row) {
      const next = !row.is_active
      this.$confirm('确定' + (next ? '启用' : '停用') + '账号【' + row.username + '】吗?', '提示', { type: 'warning' })
        .then(async () => {
          const { data } = await updateAccount(row.id, { is_active: next })
          if (data.code === 0) { this.$message.success('操作成功'); this.load() }
        }).catch(() => {})
    }
  }
}
</script>
