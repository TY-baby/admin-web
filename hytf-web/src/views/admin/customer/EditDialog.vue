<template>
  <el-dialog :title="title" :visible.sync="visible" width="720px" :close-on-click-modal="false">
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
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" maxlength="255" />
        </el-form-item>
        <el-divider content-position="left">抖音号信息（可添加多个）</el-divider>
        <div v-for="(d, idx) in form.douyin_list" :key="idx" class="dy-row">
          <el-row :gutter="8">
            <el-col :span="12">
              <el-form-item label="抖音号ID" :prop="'douyin_list.'+idx+'.douyin_id'" :rules="rules.douyin_id">
                <el-input v-model="d.douyin_id" maxlength="50" placeholder="唯一标识" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="抖音号名称">
                <el-input v-model="d.douyin_name" maxlength="50" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="充值金额" :prop="'douyin_list.'+idx+'.recharge_amount'" :rules="rules.recharge_amount">
                <el-input v-model="d.recharge_amount" placeholder="正整数,单位元" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="授权时间">
                <el-select v-model="d.auth_duration" style="width:100%">
                  <el-option label="不限" value="UNLIMITED" />
                  <el-option label="3天" value="D3" />
                  <el-option label="7天" value="D7" />
                  <el-option label="30天" value="D30" />
                  <el-option label="自定义" value="CUSTOM" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12" v-if="d.auth_duration === 'CUSTOM'">
              <el-form-item label="自定义天数">
                <el-input-number v-model="d.auth_days_custom" :min="1" :max="3650" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="档位预览">
                <el-tag>{{ tierOf(d.recharge_amount) }}</el-tag>
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="备注">
                <el-input v-model="d.remark" maxlength="255" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-button v-if="form.douyin_list.length > 1" size="mini" type="danger" plain
                     icon="el-icon-delete" @click="form.douyin_list.splice(idx,1)"
                     style="margin-bottom:12px">移除该抖音号</el-button>
          <el-divider v-if="idx < form.douyin_list.length - 1" />
        </div>
        <el-button size="mini" type="primary" plain icon="el-icon-plus" @click="addDouyin">添加抖音号</el-button>
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
        <el-form-item label="抖音号名称">
          <el-input v-model="form.douyin_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="充值金额">
          <el-input v-model="form.recharge_amount" />
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
import { isPhone, isPositiveInt } from '@/utils/validate'

const emptyDouyin = () => ({
  douyin_id: '', douyin_name: '', recharge_amount: '',
  auth_duration: 'UNLIMITED', auth_days_custom: null, remark: ''
})

export default {
  name: 'EditDialog',
  data() {
    return {
      visible: false, saving: false, mode: 'create', title: '新增客户',
      customerId: null, accountId: null,
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
        douyin_id: [
          { required: true, message: '请输入抖音号ID', trigger: 'blur' },
          { max: 50, message: '不超过50字符', trigger: 'blur' }
        ],
        recharge_amount: [
          { required: true, message: '请输入充值金额', trigger: 'blur' },
          { validator: (r, v, cb) => isPositiveInt(v) ? cb() : cb(new Error('请输入正整数')), trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    buildEmpty() {
      return {
        customer_name: '', contact_name: '', phone: '', remark: '',
        douyin_list: [emptyDouyin()], is_active_inv: true,
        douyin_name: '', recharge_amount: '', auth_duration: 'UNLIMITED',
        auth_days_custom: null, status: 'NORMAL'
      }
    },
    addDouyin() { this.form.douyin_list.push(emptyDouyin()) },
    tierOf(v) {
      const n = Number(v)
      if (!n || n < 200) return 'A(300/天)'
      if (n < 500) return 'B(600/天)'
      return 'C(1000/天)'
    },
    open(row, acc, appendMode) {
      this.form = this.buildEmpty()
      this.customerId = row ? row.id : null
      this.accountId = acc ? acc.id : null
      if (!row) {
        this.mode = 'create'; this.title = '新增客户'
      } else if (appendMode) {
        this.mode = 'append'
        this.title = '为客户【' + row.customer_name + '】追加抖音号'
        this.form.customer_name = row.customer_name
        this.form.contact_name = row.contact_name
        this.form.phone = row.phone
      } else if (acc) {
        this.mode = 'editDouyin'
        this.title = '编辑抖音号【' + acc.douyin_id + '】'
        this.form.douyin_name = acc.douyin_name
        this.form.recharge_amount = String(acc.recharge_amount)
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
        this.saving = true
        try {
          if (this.mode === 'create' || this.mode === 'append') {
            const payload = {
              customer_name: this.form.customer_name,
              contact_name: this.form.contact_name,
              phone: this.form.phone,
              remark: this.form.remark,
              douyin_list: this.form.douyin_list.map(d => ({ ...d, recharge_amount: Number(d.recharge_amount) }))
            }
            const { data } = await createCustomer(payload)
            if (data.code === 0) { this.$message.success('保存成功'); this.visible = false; this.$emit('ok') }
          } else if (this.mode === 'editCustomer') {
            const { data } = await updateCustomer(this.customerId, {
              customer_name: this.form.customer_name,
              contact_name: this.form.contact_name,
              remark: this.form.remark,
              is_active: this.form.is_active_inv
            })
            if (data.code === 0) { this.$message.success('已保存'); this.visible = false; this.$emit('ok') }
          } else if (this.mode === 'editDouyin') {
            const { data } = await updateDouyin(this.accountId, {
              douyin_name: this.form.douyin_name,
              recharge_amount: Number(this.form.recharge_amount),
              auth_duration: this.form.auth_duration,
              auth_days_custom: this.form.auth_days_custom,
              status: this.form.status,
              remark: this.form.remark
            })
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
</style>