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
  {
    path: '/customer',
    component: Layout,
    meta: { title: '客户管理', icon: 'el-icon-user' },
    children: [
      { path: 'list', name: 'CustomerList', component: () => import('@/views/customer/index.vue'), meta: { title: '客户列表' } },
      { path: 'detail/:id', name: 'CustomerDetail', component: () => import('@/views/customer/detail.vue'), meta: { title: '客户详情' }, hidden: true }
    ]
  },
  {
    path: '/business',
    component: Layout,
    meta: { title: '商机管理', icon: 'el-icon-s-flag' },
    children: [
      { path: 'opportunity', name: 'Opportunity', component: () => import('@/views/opportunity/index.vue'), meta: { title: '商机列表' } }
    ]
  },
  {
    path: '/order',
    component: Layout,
    meta: { title: '订单管理', icon: 'el-icon-s-order' },
    children: [
      { path: 'list', name: 'OrderList', component: () => import('@/views/order/index.vue'), meta: { title: '订单列表' } }
    ]
  },
  {
    path: '/digest',
    component: Layout,
    meta: { title: '消化跟进', icon: 'el-icon-phone' },
    children: [
      { path: 'follow', name: 'FollowList', component: () => import('@/views/follow/index.vue'), meta: { title: '跟进记录' } },
      { path: 'product', name: 'ProductList', component: () => import('@/views/product/index.vue'), meta: { title: '产品资料' } }
    ]
  },
  {
    path: '/vip',
    component: Layout,
    meta: { title: 'VIP会员', icon: 'el-icon-s-finance' },
    children: [
      { path: 'member', name: 'VipMember', component: () => import('@/views/vip/index.vue'), meta: { title: '会员管理' } }
    ]
  },
  {
    path: '/workflow',
    component: Layout,
    meta: { title: '流程引擎', icon: 'el-icon-s-claim' },
    children: [
      { path: 'list', name: 'WorkflowList', component: () => import('@/views/workflow/index.vue'), meta: { title: '流程管理' } }
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
