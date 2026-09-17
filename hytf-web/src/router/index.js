import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/client/login' },
  { path: '/client/login', name: 'ClientLogin', component: () => import('@/views/client/Login.vue'), meta: { title: '鎭掕€€寮曟搸|鎭掕€€鎶曟斁' } },
  { path: '/client/home', name: 'ClientHome', component: () => import('@/views/client/Home.vue'), meta: { title: '棣栭〉' } },
  { path: '/client/launch', name: 'ClientLaunch', component: () => import('@/views/client/Launch.vue'), meta: { title: '鎶曟斁鏁版嵁' } },
  { path: '/client/finance', name: 'ClientFinance', component: () => import('@/views/client/Finance.vue'), meta: { title: '璐㈠姟' } },
  { path: '/admin/login', name: 'AdminLogin', component: () => import('@/views/admin/Login.vue'), meta: { title: '鎭掕€€CRM-绠＄悊绔? } },
  {
    path: '/admin',
    component: () => import('@/layout/AdminLayout.vue'),
    redirect: '/admin/dashboard',
    children: [
      { path: 'dashboard', name: 'AdminDashboard', component: () => import('@/views/admin/Dashboard.vue'), meta: { title: '棣栭〉' } },
      { path: 'customer', name: 'AdminCustomer', component: () => import('@/views/admin/customer/Index.vue'), meta: { title: '鐢ㄦ埛绠＄悊' } },
      { path: 'invoice', name: 'AdminInvoice', component: () => import('@/views/admin/invoice/Index.vue'), meta: { title: '寮€绁ㄧ鐞? } }
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