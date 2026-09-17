import router from './router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { getClientToken, getAdminToken } from './utils/auth'

NProgress.configure({ showSpinner: false })

router.beforeEach((to, from, next) => {
  NProgress.start()
  document.title = (to.meta && to.meta.title) ? to.meta.title : '恒耀引擎'
  const isClient = to.path.startsWith('/client')
  const isAdmin = to.path.startsWith('/admin')
  if (isClient && to.path !== '/client/login' && !getClientToken()) return next('/client/login')
  if (isAdmin && to.path !== '/admin/login' && !getAdminToken()) return next('/admin/login')
  next()
})

router.afterEach(() => NProgress.done())