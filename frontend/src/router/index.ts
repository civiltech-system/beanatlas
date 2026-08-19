import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: () => import('@/views/HomeView.vue') },
    { path: '/origins', component: () => import('@/views/OriginsView.vue') },
    { path: '/origins/:slug', component: () => import('@/views/OriginDetailView.vue') },
    { path: '/login', component: () => import('@/views/LoginView.vue') },
    { path: '/records', component: () => import('@/views/RecordsView.vue'), meta: { requiresAuth: true } },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  await auth.initialize()
  if (to.meta.requiresAuth && !auth.user) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if (to.path === '/login' && auth.user) return '/records'
})

export default router
