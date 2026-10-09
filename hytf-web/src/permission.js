import router from './router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { getClientToken, getAdminToken, getAdminInfo } from './utils/auth'

NProgress.configure({ showSpinner: false })

function adminMenuAllowed(menuKey) {
  if (!menuKey) return true
  const info = getAdminInfo()
  return (info.menus || []).indexOf(menuKey) >= 0
}

router.beforeEach((to, from, next) => {
  NProgress.start()
  document.title = (to.meta && to.meta.title) ? to.meta.title : '恒耀引擎'
  const isClient = to.path.startsWith('/client')
  const isAdmin = to.path.startsWith('/admin')
  if (isClient && to.path !== '/client/login' && !getClientToken()) return next('/client/login')
  if (isAdmin && to.path !== '/admin/login' && !getAdminToken()) return next('/admin/login')
  if (isAdmin && to.meta && to.meta.menu && !adminMenuAllowed(to.meta.menu)) {
    return next('/admin/dashboard')
  }
  next()
})

router.afterEach(() => NProgress.done())