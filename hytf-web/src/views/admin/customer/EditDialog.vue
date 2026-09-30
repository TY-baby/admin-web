<template>
  <el-dialog :title="title" :visible.sync="visible" width="780px" :close-on-click-modal="false">
    <el-form ref="form" :model="form" :rules="rules" label-width="110px" size="small">
      <template v-if="mode === 'create' || mode === 'append'">
        <el-form-item label="客户名称" prop="customer_name">
          <el-input v-model="form.customer_name" maxlength="50" show-word-limit />
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="form.contact_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" maxlength="11" placeholder="A端登录账号,默认密码=手机号+123" />
        </el-form-item>
        <el-form-item label="投放平台" prop="selected_platforms">
          <el-select v-model="form.selected_platforms" multiple placeholder="请选择平台（可多选）" style="width:100%"
                     @change="onPlatformSelect">
            <el-option v-for="p in platforms" :key="p.code" :label="p.name" :value="p.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" maxlength="255" />
        </el-form-item>

        <template v-for="pcode in form.selected_platforms">
          <div :key="pcode" class="platform-section">
            <div class="dy-head">
              <el-divider content-position="left">{{ pname(pcode) }} ID信息（可添加多个）</el-divider>
              <el-button class="add-dy-btn" size="small" icon="el-icon-plus"
                         @click="addAccount(pcode)">添加{{ pname(pcode) }}ID</el-button>
            </div>
            <div v-for="(idx, n) in accountIdxByPlatform(pcode)" :key="pcode + '_' + idx" class="dy-row">
              <el-row :gutter="8">
                <el-col :span="12">
                  <el-form-item :label="pname(pcode) + ' ID'"
                                :prop="'douyin_list.' + idx + '.douyin_id'"
                                :rules="rules.douyin_id">
                    <el-input v-model="form.douyin_list[idx].douyin_id" maxlength="50" placeholder="唯一标识" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item :label="pname(pcode) + ' 名称'">
                    <el-input v-model="form.douyin_list[idx].douyin_name" maxlength="50" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="充值金额"
                                :prop="'douyin_list.' + idx + '.recharge_amount'"
                                :rules="rules.recharge_amount">
                    <el-input v-model="form.douyin_list[idx].recharge_amount" placeholder="正整数,单位元" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="授权时间">
                    <el-select v-model="form.douyin_list[idx].auth_duration" style="width:100%">
                      <el-option label="不限" value="UNLIMITED" />
                      <el-option label="3天" value="D3" />
                      <el-option label="7天" value="D7" />
                      <el-option label="30天" value="D30" />
                      <el-option label="自定义" value="CUSTOM" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12" v-if="form.douyin_list[idx].auth_duration === 'CUSTOM'">
                  <el-form-item label="自定义天数">
                    <el-input-number v-model="form.douyin_list[idx].auth_days_custom" :min="1" :max="3650" />
                  </el-form-item>
                </el-col>
                <el-col :span="24">
                  <el-form-item label="备注">
                    <el-input v-model="form.douyin_list[idx].remark" maxlength="255" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-button v-if="accountIdxByPlatform(pcode).length > 1" size="mini" type="danger" plain
                         icon="el-icon-delete" @click="removeAccount(idx)"
                         style="margin-bottom:12px">移除该ID</el-button>
              <el-divider v-if="n < accountIdxByPlatform(pcode).length - 1" />
            </div>
          </div>
        </template>
      </template>

      <template v-else-if="mode === 'editCustomer'">
        <el-form-item label="客户名称">
          <el-input v-model="form.customer_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="form.contact_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="启用状态">
          <el-switch v-model="form.is_active_inv" active-text="启用" inactive-text="禁用" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" maxlength="255" />
        </el-form-item>
      </template>

      <template v-else-if="mode === 'editDouyin'">
        <el-form-item label="ID名称">
          <el-input v-model="form.douyin_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="追加充值金额">
          <el-input v-model="form.recharge_amount" placeholder="追加金额,非覆盖（正整数,单位元）" />
        </el-form-item>
        <el-form-item label="授权类型">
          <el-select v-model="form.auth_duration" style="width:100%">
            <el-option label="不限" value="UNLIMITED" />
            <el-option label="3天" value="D3" />
            <el-option label="7天" value="D7" />
            <el-option label="30天" value="D30" />
            <el-option label="自定义" value="CUSTOM" />
          </el-select>
        </el-form-item>
        <el-form-item label="自定义天数" v-if="form.auth_duration==='CUSTOM'">
          <el-input-number v-model="form.auth_days_custom" :min="1" :max="3650" />
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio label="NORMAL">正常</el-radio>
            <el-radio label="DISABLED">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" maxlength="255" />
        </el-form-item>
      </template>
    </el-form>
    <div slot="footer">
      <el-button size="small" @click="visible=false">取消</el-button>
      <el-button size="small" type="primary" :loading="saving" @click="submit">保存</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { createCustomer, updateCustomer, updateDouyin } from '@/api/adminCustomer'
import { getPlatforms } from '@/api/clientHome'
import { isPhone, isPositiveInt } from '@/utils/validate'

const emptyAccount = (platform) => ({
  platform_code: platform || '', douyin_id: '', douyin_name: '', recharge_amount: '',
  auth_duration: 'UNLIMITED', auth_days_custom: null, remark: ''
})

export default {
  name: 'EditDialog',
  data() {
    return {
      visible: false, saving: false, mode: 'create', title: '新增客户',
      customerId: null, accountId: null, platforms: [],
      form: this.buildEmpty(),
      rules: {
        customer_name: [
          { required: true, message: '请输入客户名称', trigger: 'blur' },
          { max: 50, message: '不超过50字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { validator: (r, v, cb) => isPhone(v) ? cb() : cb(new Error('手机号格式不正确')), trigger: 'blur' }
        ],
        selected_platforms: [
          { required: true, type: 'array', min: 1, message: '请至少选择一个平台', trigger: 'change' }
        ],
        douyin_id: [
          { required: true, message: '请输入ID', trigger: 'blur' },
          { max: 50, message: '不超过50字符', trigger: 'blur' }
        ],
        recharge_amount: [
          { required: true, message: '请输入充值金额', trigger: 'blur' },
          { validator: (r, v, cb) => isPositiveInt(v) ? cb() : cb(new Error('请输入正整数')), trigger: 'blur' }
        ]
      }
    }
  },
  async created() {
    const { data } = await getPlatforms()
    if (data.code === 0) this.platforms = data.data || []
  },
  methods: {
    pname(code) {
      const p = this.platforms.find(x => x.code === code)
      return p ? p.name : code
    },
    buildEmpty() {
      return {
        customer_name: '', contact_name: '', phone: '', remark: '',
        selected_platforms: [], douyin_list: [],
        is_active_inv: true,
        douyin_name: '', recharge_amount: '', auth_duration: 'UNLIMITED',
        auth_days_custom: null, status: 'NORMAL'
      }
    },
    onPlatformSelect(codes) {
      const existing = this.form.douyin_list.filter(d => codes.includes(d.platform_code))
      codes.forEach(c => {
        if (!existing.find(d => d.platform_code === c)) {
          existing.push(emptyAccount(c))
        }
      })
      this.form.douyin_list = existing
    },
    accountIdxByPlatform(pcode) {
      const out = []
      this.form.douyin_list.forEach((d, i) => {
        if (d.platform_code === pcode) out.push(i)
      })
      return out
    },
    addAccount(pcode) {
      this.form.douyin_list.push(emptyAccount(pcode))
    },
    removeAccount(idx) {
      this.form.douyin_list.splice(idx, 1)
    },
    open(row, acc, appendMode) {
      this.form = this.buildEmpty()
      this.customerId = row ? row.id : null
      this.accountId = acc ? acc.id : null
      if (!row) {
        this.mode = 'create'; this.title = '新增客户'
      } else if (appendMode) {
        this.mode = 'append'
        this.title = '为客户【' + row.customer_name + '】追加平台'
        this.form.customer_name = row.customer_name
        this.form.contact_name = row.contact_name
        this.form.phone = row.phone
      } else if (acc) {
        this.mode = 'editDouyin'
        this.title = '编辑【' + acc.douyin_id + '】'
        this.form.douyin_name = acc.douyin_name
        this.form.recharge_amount = ''
        this.form.auth_duration = acc.auth_duration
        this.form.status = acc.status
        this.form.remark = acc.remark
      } else {
        this.mode = 'editCustomer'
        this.title = '编辑客户【' + row.customer_name + '】'
        this.form.customer_name = row.customer_name
        this.form.contact_name = row.contact_name
        this.form.remark = row.remark
        this.form.is_active_inv = row.is_active
      }
      this.visible = true
      this.$nextTick(() => this.$refs.form && this.$refs.form.clearValidate())
    },
    async submit() {
      this.$refs.form.validate(async ok => {
        if (!ok) return
        if ((this.mode === 'create' || this.mode === 'append') && !this.form.douyin_list.length) {
          this.$message.warning('请至少添加一个平台ID'); return
        }
        this.saving = true
        try {
          if (this.mode === 'create' || this.mode === 'append') {
            const payload = {
              customer_name: this.form.customer_name,
              contact_name: this.form.contact_name,
              phone: this.form.phone,
              remark: this.form.remark,
              douyin_list: this.form.douyin_list.map(d => ({
                platform_code: d.platform_code,
                douyin_id: d.douyin_id,
                douyin_name: d.douyin_name,
                recharge_amount: Number(d.recharge_amount),
                auth_duration: d.auth_duration,
                auth_days_custom: d.auth_days_custom,
                remark: d.remark
              }))
            }
            const { data } = await createCustomer(payload)
            if (data.code === 0) { this.$message.success('保存成功'); this.visible = false; this.$emit('ok') }
            else { this.$message.error(data.msg || '保存失败') }
          } else if (this.mode === 'editCustomer') {
            const { data } = await updateCustomer(this.customerId, {
              customer_name: this.form.customer_name,
              contact_name: this.form.contact_name,
              remark: this.form.remark,
              is_active: this.form.is_active_inv
            })
            if (data.code === 0) { this.$message.success('已保存'); this.visible = false; this.$emit('ok') }
          } else if (this.mode === 'editDouyin') {
            const payload = {
              douyin_name: this.form.douyin_name,
              auth_duration: this.form.auth_duration,
              auth_days_custom: this.form.auth_days_custom,
              status: this.form.status,
              remark: this.form.remark
            }
            if (this.form.recharge_amount && Number(this.form.recharge_amount) > 0) {
              payload.recharge_amount = Number(this.form.recharge_amount)
            }
            const { data } = await updateDouyin(this.accountId, payload)
            if (data.code === 0) { this.$message.success('已保存'); this.visible = false; this.$emit('ok') }
          }
        } finally { this.saving = false }
      })
    }
  }
}
</script>

<style scoped>
.dy-row { padding: 8px 0; }
.dy-head { display: flex; align-items: center; margin: 4px 0 18px; }
.dy-head .el-divider { flex: 1; margin: 0; }
.add-dy-btn {
  background: linear-gradient(90deg, #2B5CF6 0%, #4D7DFF 100%);
  border: none; color: #fff; font-weight: bold;
  box-shadow: 0 2px 10px rgba(43, 92, 246, .45);
}
.add-dy-btn:hover { opacity: .9; color: #fff; }
.platform-section { margin-bottom: 8px; }
</style>