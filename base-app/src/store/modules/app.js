// 移动端工作台模块配置（用户可自定义显示/隐藏）
const ALL_MODULES = [
  { key: 'attendance', label: '考勤打卡', icon: '⏰', color: '#4facfe', path: '/pages/oa/attendance' },
  { key: 'leave', label: '请假申请', icon: '🌴', color: '#43e97b', path: '/pages/oa/leave' },
  { key: 'expense', label: '费用报销', icon: '💰', color: '#fa709a', path: '/pages/oa/expense' },
  { key: 'approval', label: '审批中心', icon: '✅', color: '#f6d365', path: '/pages/oa/approval' },
  { key: 'notice', label: '公司公告', icon: '📢', color: '#667eea', path: '/pages/oa/notice' },
  { key: 'addressBook', label: '通讯录', icon: '📇', color: '#38f9d7', path: '/pages/oa/address-book' },
  { key: 'customer', label: '客户管理', icon: '👥', color: '#ff9a9e', path: '/pages/customer/customer' },
  { key: 'opportunity', label: '商机管理', icon: '📈', color: '#a18cd1', path: '/pages/opportunity/opportunity' },
  { key: 'order', label: '订单管理', icon: '📋', color: '#fbc2eb', path: '/pages/order/order' },
  { key: 'follow', label: '跟进记录', icon: '📞', color: '#8fd3f4', path: '/pages/follow/follow' }
]

const STORAGE_KEY = 'base_mobile_modules'

function getDefaultVisible() {
  return ['attendance', 'leave', 'expense', 'approval', 'notice', 'addressBook']
}

function loadVisible() {
  try {
    const raw = uni.getStorageSync(STORAGE_KEY)
    if (raw) return JSON.parse(raw)
  } catch (e) {}
  return getDefaultVisible()
}

export default {
  namespaced: true,
  state: {
    allModules: ALL_MODULES,
    visibleModules: loadVisible()
  },
  getters: {
    // 首页显示的模块
    homeModules(state) {
      return state.visibleModules
        .map(key => state.allModules.find(m => m.key === key))
        .filter(Boolean)
    },
    // 所有模块及是否已显示
    moduleList(state) {
      return state.allModules.map(m => ({
        ...m,
        visible: state.visibleModules.includes(m.key)
      }))
    }
  },
  mutations: {
    SET_VISIBLE(state, keys) {
      state.visibleModules = keys
      uni.setStorageSync(STORAGE_KEY, JSON.stringify(keys))
    },
    TOGGLE_MODULE(state, key) {
      const set = new Set(state.visibleModules)
      if (set.has(key)) set.delete(key)
      else set.add(key)
      const keys = Array.from(set)
      state.visibleModules = keys
      uni.setStorageSync(STORAGE_KEY, JSON.stringify(keys))
    },
    RESET(state) {
      const keys = getDefaultVisible()
      state.visibleModules = keys
      uni.setStorageSync(STORAGE_KEY, JSON.stringify(keys))
    }
  }
}
