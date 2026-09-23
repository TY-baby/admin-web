import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/client/login' },
  { path: '/client/login', name: 'ClientLogin', component: () => import('@/views/client/Login.vue'), meta: { title: '恒耀引擎|恒耀投放' } },
  { path: '/client/home', name: 'ClientHome', component: () => import('@/views/client/Home.vue'), meta: { title: '首页' } },
  { path: '/client/launch', name: 'ClientLaunch', component: () => import('@/views/client/Launch.vue'), meta: { title: '投放数据' } },
  { path: '/client/finance', name: 'ClientFinance', component: () => import('@/views/client/Finance.vue'), meta: { title: '财务' } },
  { path: '/admin/login', name: 'AdminLogin', component: () => import('@/views/admin/Login.vue'), meta: { title: '恒耀CRM-管理员' } },
  {
    path: '/admin',
    component: () => import('@/layout/AdminLayout.vue'),
    redirect: '/admin/dashboard',
    children: [
      { path: 'dashboard', name: 'AdminDashboard', component: () => import('@/views/admin/Dashboard.vue'), meta: { title: '首页' } },
      { path: 'customer', name: 'AdminCustomer', component: () => import('@/views/admin/customer/Index.vue'), meta: { title: '用户管理' } },
      { path: 'novel', name: 'AdminNovel', component: () => import('@/views/admin/novel/Index.vue'), meta: { title: '网文客户' } },
      { path: 'invoice', name: 'AdminInvoice', component: () => import('@/views/admin/invoice/Index.vue'), meta: { title: '开票管理' } }
    ]
  },
  { path: '*', redirect: '/' }
]

const router = new VueRouter({ mode: 'hash', routes })

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

export default router