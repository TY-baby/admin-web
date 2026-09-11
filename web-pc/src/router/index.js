import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: Home, meta: { title: '首页' } },
  { path: '/news', component: () => import('@/views/NewsList.vue'), meta: { title: '新闻资讯' } },
  { path: '/news/:id', component: () => import('@/views/NewsDetail.vue'), meta: { title: '新闻详情' } },
  { path: '/page/:column', component: () => import('@/views/Column.vue'), meta: { title: '栏目' } },
  { path: '*', redirect: '/' }
]

const router = new VueRouter({ mode: 'history', routes })

router.afterEach(to => {
  if (to.meta && to.meta.title) {
    document.title = to.meta.title + ' - Base Room 官网'
  }
})

export default router