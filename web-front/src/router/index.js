import Vue from 'vue'
import VueRouter from 'vue-router'
import Layout from '@/views/layout/index.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/login', component: () => import('@/views/login/index.vue'), hidden: true, meta: { title: '登录' } },
  {
    path: '/',
    component: Layout,
    redirect: '/transaction',
    children: [
      {
        path: 'transaction',
        name: 'Transaction',
        component: () => import('@/views/transaction/index.vue'),
        meta: { title: '交易信息', icon: 'el-icon-s-data' }
      }
    ]
  },
  { path: '*', redirect: '/', hidden: true }
]

const router = new VueRouter({
  mode: 'history',
  // 关键：与 publicPath / nginx location /admin/ 保持一致
  base: '/admin/',
  routes
})

router.beforeEach((to, from, next) => {
  if (to.path === '/login') return next()
  const token = localStorage.getItem('my_token')
  if (!token) return next('/login')
  next()
})

export default router