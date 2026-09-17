<template>
  <el-dialog :title="title" :visible.sync="visible" width="720px" :close-on-click-modal="false">
    <el-form ref="form" :model="form" :rules="rules" label-width="110px" size="small">
      <template v-if="mode === 'create' || mode === 'append'">
        <el-form-item label="瀹㈡埛鍚嶇О" prop="customer_name">
          <el-input v-model="form.customer_name" maxlength="50" show-word-limit />
        </el-form-item>
        <el-form-item label="鑱旂郴浜?>
          <el-input v-model="form.contact_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="鎵嬫満鍙? prop="phone">
          <el-input v-model="form.phone" maxlength="11" placeholder="A绔櫥褰曡处鍙?榛樿瀵嗙爜=鎵嬫満鍙?123" />
        </el-form-item>
        <el-form-item label="澶囨敞">
          <el-input v-model="form.remark" type="textarea" :rows="2" maxlength="255" />
        </el-form-item>
        <el-divider content-position="left">鎶栭煶鍙蜂俊鎭紙鍙坊鍔犲涓級</el-divider>
        <div v-for="(d, idx) in form.douyin_list" :key="idx" class="dy-row">
          <el-row :gutter="8">
            <el-col :span="12">
              <el-form-item label="鎶栭煶鍙稩D" :prop="'douyin_list.'+idx+'.douyin_id'" :rules="rules.douyin_id">
                <el-input v-model="d.douyin_id" maxlength="50" placeholder="鍞竴鏍囪瘑" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="鎶栭煶鍙峰悕绉?>
                <el-input v-model="d.douyin_name" maxlength="50" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="鍏呭€奸噾棰? :prop="'douyin_list.'+idx+'.recharge_amount'" :rules="rules.recharge_amount">
                <el-input v-model="d.recharge_amount" placeholder="姝ｆ暣鏁?鍗曚綅鍏? />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="鎺堟潈鏃堕棿">
                <el-select v-model="d.auth_duration" style="width:100%">
                  <el-option label="涓嶉檺" value="UNLIMITED" />
                  <el-option label="3澶? value="D3" />
                  <el-option label="7澶? value="D7" />
                  <el-option label="30澶? value="D30" />
                  <el-option label="鑷畾涔? value="CUSTOM" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12" v-if="d.auth_duration === 'CUSTOM'">
              <el-form-item label="鑷畾涔夊ぉ鏁?>
                <el-input-number v-model="d.auth_days_custom" :min="1" :max="3650" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="妗ｄ綅棰勮">
                <el-tag>{{ tierOf(d.recharge_amount) }}</el-tag>
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="澶囨敞">
                <el-input v-model="d.remark" maxlength="255" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-button v-if="form.douyin_list.length > 1" size="mini" type="danger" plain
                     icon="el-icon-delete" @click="form.douyin_list.splice(idx,1)"
                     style="margin-bottom:12px">绉婚櫎璇ユ姈闊冲彿</el-button>
          <el-divider v-if="idx < form.douyin_list.length - 1" />
        </div>
        <el-button size="mini" type="primary" plain icon="el-icon-plus" @click="addDouyin">娣诲姞鎶栭煶鍙?/el-button>
      </template>

      <template v-else-if="mode === 'editCustomer'">
        <el-form-item label="瀹㈡埛鍚嶇О">
          <el-input v-model="form.customer_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="鑱旂郴浜?>
          <el-input v-model="form.contact_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="鍚敤鐘舵€?>
          <el-switch v-model="form.is_active_inv" active-text="鍚敤" inactive-text="绂佺敤" />
        </el-form-item>
        <el-form-item label="澶囨敞">
          <el-input v-model="form.remark" type="textarea" :rows="2" maxlength="255" />
        </el-form-item>
      </template>

      <template v-else-if="mode === 'editDouyin'">
        <el-form-item label="鎶栭煶鍙峰悕绉?>
          <el-input v-model="form.douyin_name" maxlength="50" />
        </el-form-item>
        <el-form-item label="鍏呭€奸噾棰?>
          <el-input v-model="form.recharge_amount" />
        </el-form-item>
        <el-form-item label="鎺堟潈绫诲瀷">
          <el-select v-model="form.auth_duration" style="width:100%">
            <el-option label="涓嶉檺" value="UNLIMITED" />
            <el-option label="3澶? value="D3" />
            <el-option label="7澶? value="D7" />
            <el-option label="30澶? value="D30" />
            <el-option label="鑷畾涔? value="CUSTOM" />
          </el-select>
        </el-form-item>
        <el-form-item label="鑷畾涔夊ぉ鏁? v-if="form.auth_duration==='CUSTOM'">
          <el-input-number v-model="form.auth_days_custom" :min="1" :max="3650" />
        </el-form-item>
        <el-form-item label="鐘舵€?>
          <el-radio-group v-model="form.status">
            <el-radio label="NORMAL">姝ｅ父</el-radio>
            <el-radio label="DISABLED">绂佺敤</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="澶囨敞">
          <el-input v-model="form.remark" type="textarea" :rows="2" maxlength="255" />
        </el-form-item>
      </template>
    </el-form>
    <div slot="footer">
      <el-button size="small" @click="visible=false">鍙栨秷</el-button>
      <el-button size="small" type="primary" :loading="saving" @click="submit">淇濆瓨</el-button>
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
      visible: false, saving: false, mode: 'create', title: '鏂板瀹㈡埛',
      customerId: null, accountId: null,
      form: this.buildEmpty(),
      rules: {
        customer_name: [
          { required: true, message: '璇疯緭鍏ュ鎴峰悕绉?, trigger: 'blur' },
          { max: 50, message: '涓嶈秴杩?0瀛楃', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '璇疯緭鍏ユ墜鏈哄彿', trigger: 'blur' },
          { validator: (r, v, cb) => isPhone(v) ? cb() : cb(new Error('鎵嬫満鍙锋牸寮忎笉姝ｇ‘')), trigger: 'blur' }
        ],
        douyin_id: [
          { required: true, message: '璇疯緭鍏ユ姈闊冲彿ID', trigger: 'blur' },
          { max: 50, message: '涓嶈秴杩?0瀛楃', trigger: 'blur' }
        ],
        recharge_amount: [
          { required: true, message: '璇疯緭鍏ュ厖鍊奸噾棰?, trigger: 'blur' },
          { validator: (r, v, cb) => isPositiveInt(v) ? cb() : cb(new Error('璇疯緭鍏ユ鏁存暟')), trigger: 'blur' }
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
      if (!n || n < 200) return 'A(300/澶?'
      if (n < 500) return 'B(600/澶?'
      return 'C(1000/澶?'
    },
    open(row, acc, appendMode) {
      this.form = this.buildEmpty()
      this.customerId = row ? row.id : null
      this.accountId = acc ? acc.id : null
      if (!row) {
        this.mode = 'create'; this.title = '鏂板瀹㈡埛'
      } else if (appendMode) {
        this.mode = 'append'
        this.title = '涓哄鎴枫€? + row.customer_name + '銆戣拷鍔犳姈闊冲彿'
        this.form.customer_name = row.customer_name
        this.form.contact_name = row.contact_name
        this.form.phone = row.phone
      } else if (acc) {
        this.mode = 'editDouyin'
        this.title = '缂栬緫鎶栭煶鍙枫€? + acc.douyin_id + '銆?
        this.form.douyin_name = acc.douyin_name
        this.form.recharge_amount = String(acc.recharge_amount)
        this.form.auth_duration = acc.auth_duration
        this.form.status = acc.status
        this.form.remark = acc.remark
      } else {
        this.mode = 'editCustomer'
        this.title = '缂栬緫瀹㈡埛銆? + row.customer_name + '銆?
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
            if (data.code === 0) { this.$message.success('淇濆瓨鎴愬姛'); this.visible = false; this.$emit('ok') }
          } else if (this.mode === 'editCustomer') {
            const { data } = await updateCustomer(this.customerId, {
              customer_name: this.form.customer_name,
              contact_name: this.form.contact_name,
              remark: this.form.remark,
              is_active: this.form.is_active_inv
            })
            if (data.code === 0) { this.$message.success('宸蹭繚瀛?); this.visible = false; this.$emit('ok') }
          } else if (this.mode === 'editDouyin') {
            const { data } = await updateDouyin(this.accountId, {
              douyin_name: this.form.douyin_name,
              recharge_amount: Number(this.form.recharge_amount),
              auth_duration: this.form.auth_duration,
              auth_days_custom: this.form.auth_days_custom,
              status: this.form.status,
              remark: this.form.remark
            })
            if (data.code === 0) { this.$message.success('宸蹭繚瀛?); this.visible = false; this.$emit('ok') }
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