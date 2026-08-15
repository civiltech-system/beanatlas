<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { Origin } from '@/types/origin'
import { fetchOrigin } from '@/api/origins'
import { useOriginsStore } from '@/stores/origins'
import FlavorIndicator from '@/components/FlavorIndicator.vue'
import FlavorRadar from '@/components/FlavorRadar.vue'
import OriginCard from '@/components/OriginCard.vue'
import { usePageMeta } from '@/composables/usePageMeta'
import { useLocale } from '@/composables/useLocale'

const route = useRoute()
const origin = ref<Origin | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const { translateTerm } = useLocale()
const originsStore = useOriginsStore()

onMounted(async () => {
  try {
    origin.value = await fetchOrigin(route.params.slug as string)
  } catch {
    error.value = 'Origin not found'
  } finally {
    loading.value = false
  }
  originsStore.loadOrigins()
})

const relatedOrigins = computed(() => {
  const current = origin.value
  if (!current) return []
  return originsStore.origins
    .filter((o) => o.slug !== current.slug)
    .map((o) => {
      const sharedFlavors = o.flavor_notes.filter((note) => current.flavor_notes.includes(note)).length
      const sameRegion = o.region === current.region ? 2 : 0
      return { origin: o, score: sameRegion + sharedFlavors }
    })
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 3)
    .map((entry) => entry.origin)
})

usePageMeta(() => {
  const o = origin.value
  if (!o) {
    return { title: '産地情報', description: '世界のコーヒー産地の詳細情報。', path: route.path }
  }
  const region = translateTerm(o.region)
  const varieties = o.varieties.slice(0, 3).map(translateTerm).join('、')
  const processes = o.process_methods.slice(0, 2).map(translateTerm).join('、')
  const notes = o.flavor_notes.slice(0, 3).map(translateTerm).join('、')
  return {
    title: `${o.country_ja}のコーヒー産地ガイド｜品種・精製・フレーバー`,
    description:
      `${o.country_ja}（${region}）、標高${o.altitude_min}〜${o.altitude_max}mのコーヒー産地情報。` +
      `品種は${varieties || '複数種'}、精製方法は${processes || '複数種'}。` +
      `フレーバーノート: ${notes || '多彩な味わい'}。`,
    path: route.path,
  }
})
</script>

<template>
  <div class="max-w-3xl mx-auto px-6 py-12">
    <div v-if="loading" class="text-coffee-400 text-center py-12">Loading...</div>
    <div v-else-if="error" class="text-red-500 text-center py-12">{{ error }}</div>

    <template v-else-if="origin">
      <!-- Header -->
      <div class="mb-8">
        <p class="text-origin-green text-sm font-medium mb-1">{{ origin.region }}</p>
        <h1 class="text-4xl font-serif font-bold text-coffee-600">{{ origin.country }}</h1>
        <p class="text-coffee-400 mt-2">{{ origin.altitude_min }}–{{ origin.altitude_max }}m · {{ origin.climate }}</p>
      </div>

      <!-- Flavor Profile -->
      <div class="bg-white rounded-2xl p-6 shadow-sm mb-6">
        <h2 class="text-lg font-semibold text-coffee-600 mb-4">Flavor Profile</h2>
        <div class="flex flex-col sm:flex-row items-center gap-6">
          <FlavorRadar
            :acidity="origin.acidity"
            :bitterness="origin.bitterness"
            :sweetness="origin.sweetness"
            :body="origin.body"
            class="w-44 flex-shrink-0"
          />
          <div class="space-y-3 flex-1 w-full">
            <FlavorIndicator label="Acidity" :value="origin.acidity" />
            <FlavorIndicator label="Bitterness" :value="origin.bitterness" />
            <FlavorIndicator label="Sweetness" :value="origin.sweetness" />
            <FlavorIndicator label="Body" :value="origin.body" />
          </div>
        </div>
      </div>

      <!-- Flavor Notes -->
      <div class="mb-6">
        <h2 class="text-lg font-semibold text-coffee-600 mb-3">Flavor Notes</h2>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="note in origin.flavor_notes"
            :key="note"
            class="bg-coffee-100 text-coffee-600 text-xs px-3 py-1 rounded-full"
          >{{ note }}</span>
        </div>
      </div>

      <!-- Info Grid -->
      <div class="grid grid-cols-2 gap-4 mb-8">
        <div class="bg-white rounded-xl p-4 shadow-sm">
          <p class="text-xs text-coffee-400 mb-1">Varieties</p>
          <p class="text-sm text-coffee-600">{{ origin.varieties.join(', ') || '—' }}</p>
        </div>
        <div class="bg-white rounded-xl p-4 shadow-sm">
          <p class="text-xs text-coffee-400 mb-1">Process Methods</p>
          <p class="text-sm text-coffee-600">{{ origin.process_methods.join(', ') || '—' }}</p>
        </div>
      </div>

      <!-- Description -->
      <div class="prose prose-coffee max-w-none mb-8">
        <p class="text-coffee-600 leading-relaxed">{{ origin.description }}</p>
      </div>

      <!-- Related Origins -->
      <div v-if="relatedOrigins.length" class="mb-8">
        <h2 class="text-lg font-semibold text-coffee-600 mb-3">似た産地</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <OriginCard v-for="related in relatedOrigins" :key="related.id" :origin="related" />
        </div>
      </div>

      <!-- Back -->
      <RouterLink to="/origins" class="text-sm text-coffee-400 hover:text-coffee-600 transition-colors">
        ← Back to Origins
      </RouterLink>
    </template>
  </div>
</template>
