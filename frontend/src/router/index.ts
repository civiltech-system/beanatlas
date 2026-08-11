import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: () => import('@/views/HomeView.vue') },
    { path: '/origins', component: () => import('@/views/OriginsView.vue') },
    { path: '/origins/:slug', component: () => import('@/views/OriginDetailView.vue') },
  ],
})

export default router
