<script setup lang="ts">
import { onMounted } from 'vue'
import { useOriginsStore } from '@/stores/origins'
import OriginCard from '@/components/OriginCard.vue'
import { usePageMeta } from '@/composables/usePageMeta'

const store = useOriginsStore()
onMounted(() => store.loadOrigins())

usePageMeta({
  title: 'コーヒー産地一覧',
  description:
    'エチオピア、コロンビア、ブラジルなど世界各地のコーヒー産地を一覧で紹介。産地ごとの気候・標高・フレーバープロファイルを比較できます。',
  path: '/origins',
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-6 py-12">
    <h1 class="text-3xl font-serif font-bold text-coffee-600 mb-8">Coffee Origins</h1>

    <div v-if="store.loading" class="text-coffee-400 text-center py-12">Loading...</div>
    <div v-else-if="store.error" class="text-red-500 text-center py-12">{{ store.error }}</div>
    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <OriginCard v-for="origin in store.origins" :key="origin.id" :origin="origin" />
    </div>
  </div>
</template>
