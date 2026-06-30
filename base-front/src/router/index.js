import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/views/layout/index.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/login', component: () => import('@/views/login/index.vue'), hidden: true },
  { path: '/bigscreen/fullscreen', component: () => import('@/views/bigscreen/full.vue') },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/index.vue'), meta: { title: '工作台', icon: 'el-icon-s-home' } }
    ]
  },
  // CRM 客户管理
  {
    path: '/crm',
    component: Layout,
    redirect: '/crm/customer',
    meta: { title: 'CRM', icon: 'el-icon-s-custom' },
    children: [
      { path: 'customer', name: 'CrmCustomer', component: () => import('@/views/customer/index.vue'), meta: { title: '客户管理' } },
      { path: 'customer/detail/:id', name: 'CrmCustomerDetail', component: () => import('@/views/customer/detail.vue'), meta: { title: '客户详情' }, hidden: true },
      { path: 'opportunity', name: 'CrmOpportunity', component: () => import('@/views/opportunity/index.vue'), meta: { title: '商机管理' } },
      { path: 'order', name: 'CrmOrder', component: () => import('@/views/order/index.vue'), meta: { title: '订单管理' } },
      { path: 'follow', name: 'CrmFollow', component: () => import('@/views/follow/index.vue'), meta: { title: '跟进记录' } },
      { path: 'product', name: 'CrmProduct', component: () => import('@/views/product/index.vue'), meta: { title: '产品资料' } },
      { path: 'vip', name: 'CrmVip', component: () => import('@/views/vip/index.vue'), meta: { title: 'VIP会员' } },
      { path: 'workflow', name: 'CrmWorkflow', component: () => import('@/views/workflow/index.vue'), meta: { title: '流程引擎' } }
    ]
  },

  // ERP 企业资源计划
  {
    path: '/erp',
    component: Layout,
    redirect: '/erp/dashboard',
    meta: { title: 'ERP', icon: 'el-icon-s-shop' },
    children: [
      { path: 'dashboard', name: 'ErpDashboard', component: () => import('@/views/erp/dashboard.vue'), meta: { title: 'ERP概览' } },
      { path: 'purchase', name: 'ErpPurchase', component: () => import('@/views/erp/purchase.vue'), meta: { title: '采购管理' } },
      { path: 'supplier', name: 'ErpSupplier', component: () => import('@/views/erp/supplier.vue'), meta: { title: '供应商管理' } },
      { path: 'inventory', name: 'ErpInventory', component: () => import('@/views/erp/inventory.vue'), meta: { title: '库存管理' } },
      { path: 'warehouse', name: 'ErpWarehouse', component: () => import('@/views/erp/warehouse.vue'), meta: { title: '仓库管理' } },
      { path: 'production', name: 'ErpProduction', component: () => import('@/views/erp/production.vue'), meta: { title: '生产管理' } },
      { path: 'sales', name: 'ErpSales', component: () => import('@/views/erp/sales.vue'), meta: { title: '销售管理' } },
      { path: 'finance', name: 'ErpFinance', component: () => import('@/views/erp/finance.vue'), meta: { title: '财务管理' } },
      { path: 'hr', name: 'ErpHr', component: () => import('@/views/erp/hr.vue'), meta: { title: '人事管理' } },
      { path: 'report', name: 'ErpReport', component: () => import('@/views/erp/report.vue'), meta: { title: '报表中心' } }
    ]
  },

  // OA 办公自动化
  {
    path: '/oa',
    component: Layout,
    redirect: '/oa/dashboard',
    meta: { title: 'OA', icon: 'el-icon-s-check' },
    children: [
      { path: 'dashboard', name: 'OaDashboard', component: () => import('@/views/oa/dashboard.vue'), meta: { title: 'OA概览' } },
      { path: 'attendance', name: 'OaAttendance', component: () => import('@/views/oa/attendance.vue'), meta: { title: '考勤管理' } },
      { path: 'leave', name: 'OaLeave', component: () => import('@/views/oa/leave.vue'), meta: { title: '请假审批' } },
      { path: 'expense', name: 'OaExpense', component: () => import('@/views/oa/expense.vue'), meta: { title: '费用报销' } },
      { path: 'meeting', name: 'OaMeeting', component: () => import('@/views/oa/meeting.vue'), meta: { title: '会议室' } },
      { path: 'notice', name: 'OaNotice', component: () => import('@/views/oa/notice.vue'), meta: { title: '通知公告' } },
      { path: 'task', name: 'OaTask', component: () => import('@/views/oa/task.vue'), meta: { title: '任务协作' } },
      { path: 'document', name: 'OaDocument', component: () => import('@/views/oa/document.vue'), meta: { title: '文档中心' } },
      { path: 'organization', name: 'OaOrganization', component: () => import('@/views/oa/organization.vue'), meta: { title: '组织架构' } },
      { path: 'address-book', name: 'OaAddressBook', component: () => import('@/views/oa/address-book.vue'), meta: { title: '通讯录' } },
      { path: 'vehicle', name: 'OaVehicle', component: () => import('@/views/oa/vehicle.vue'), meta: { title: '车辆管理' } },
      { path: 'recruit', name: 'OaRecruit', component: () => import('@/views/oa/recruit.vue'), meta: { title: '招聘管理' } }
    ]
  },

  {
    path: '/bigscreen',
    component: Layout,
    redirect: '/bigscreen/sales',
    meta: { title: '大屏展示', icon: 'el-icon-data-board' },
    children: [
      { path: 'sales', name: 'BigscreenSales', component: () => import('@/views/bigscreen/sales/index.vue'), meta: { title: '销售轮播大屏' } },
      { path: 'abnormal', name: 'BigscreenAbnormal', component: () => import('@/views/bigscreen/abnormal/index.vue'), meta: { title: '异常管理驾驶舱' } },
      { path: 'chemical', name: 'BigscreenChemical', component: () => import('@/views/bigscreen/chemical/index.vue'), meta: { title: '化工生产监控' } },
      { path: 'sales-rank', name: 'BigscreenSalesRank', component: () => import('@/views/bigscreen/sales-rank/index.vue'), meta: { title: '销售业绩看板' } },
      { path: 'aviation', name: 'BigscreenAviation', component: () => import('@/views/bigscreen/aviation/index.vue'), meta: { title: '航空运营监控' } },
      { path: 'hse', name: 'BigscreenHse', component: () => import('@/views/bigscreen/hse/index.vue'), meta: { title: '园区HSE' } }
    ]
  },
  {
    path: '/plate',
    component: Layout,
    redirect: '/plate/image-detect',
    meta: { title: '车牌识别', icon: 'el-icon-camera-solid' },
    children: [
      { path: 'image-detect', name: 'PlateImageDetect', component: () => import('@/views/plate/image-detect.vue'), meta: { title: '图片车牌检测' } },
      { path: 'video-detect', name: 'PlateVideoDetect', component: () => import('@/views/plate/video-detect.vue'), meta: { title: '视频车牌检测' } },
      { path: 'image-resource', name: 'PlateImageResource', component: () => import('@/views/plate/image-resource.vue'), meta: { title: '图片资源管理' } },
      { path: 'video-resource', name: 'PlateVideoResource', component: () => import('@/views/plate/video-resource.vue'), meta: { title: '视频资源管理' } },
      { path: 'data-visualization', name: 'PlateDataVisualization', component: () => import('@/views/plate/data-visualization.vue'), meta: { title: '数据可视化大屏' } },
      { path: 'system-monitor', name: 'PlateSystemMonitor', component: () => import('@/views/plate/system-monitor.vue'), meta: { title: '系统监控' } },
      { path: 'system-logs', name: 'PlateSystemLogs', component: () => import('@/views/plate/system-logs.vue'), meta: { title: '系统日志' } },
      { path: 'project-docs', name: 'PlateProjectDocs', component: () => import('@/views/plate/project-docs.vue'), meta: { title: '项目文档' } },
      { path: 'model-manage', name: 'PlateModelManage', component: () => import('@/views/plate/model-manage.vue'), meta: { title: '模型管理' } },
      { path: 'llm-chat', name: 'PlateLlmChat', component: () => import('@/views/plate/llm-chat.vue'), meta: { title: '大模型聊天' } },
      { path: 'multimodal-chat', name: 'PlateMultimodalChat', component: () => import('@/views/plate/multimodal-chat.vue'), meta: { title: '多模态问答' } }
    ]
  },
  { path: '*', redirect: '/' }
]

const router = new VueRouter({ mode: 'history', routes })

router.beforeEach((to, from, next) => {
  if (to.path === '/login' || to.path.startsWith('/bigscreen/fullscreen')) return next()
  const token = localStorage.getItem('base_token')
  if (!token) return next('/login')
  next()
})

export default router
