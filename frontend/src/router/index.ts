import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/origins', component: () => import('@/views/OriginsView.vue') },
    { path: '/origins/:slug', component: () => import('@/views/OriginDetailView.vue') },
  ],
})

export default router
