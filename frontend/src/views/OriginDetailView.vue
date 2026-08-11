<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { Origin } from '@/types/origin'
import { fetchOrigin } from '@/api/origins'
import FlavorRadar from '@/components/FlavorRadar.vue'
import { useLocale } from '@/composables/useLocale'

const route = useRoute()
const origin = ref<Origin | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const { locale, t, translateTerm } = useLocale()

onMounted(async () => {
  try {
    origin.value = await fetchOrigin(route.params.slug as string)
  } catch {
    error.value = 'Origin not found'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="max-w-3xl mx-auto px-6 py-12">
    <div v-if="loading" class="text-coffee-400 text-center py-12">{{ t('detail.loading') }}</div>
    <div v-else-if="error" class="text-red-500 text-center py-12">{{ t('detail.notFound') }}</div>

    <template v-else-if="origin">
      <!-- Header -->
      <div class="mb-8">
        <p class="text-origin-green text-sm font-medium mb-1">
          {{ origin.region }}
          <span v-if="origin.sub_region" class="text-coffee-300"> › {{ origin.sub_region }}</span>
        </p>
        <h1 class="text-4xl font-serif font-bold text-coffee-600">
          {{ locale === 'ja' ? origin.country_ja : origin.country }}
        </h1>
        <p v-if="origin.farm" class="text-coffee-500 text-sm mt-1">
          {{ t('detail.farm') }}: {{ origin.farm }}
        </p>
        <p class="text-coffee-400 mt-2">{{ origin.altitude_min }}–{{ origin.altitude_max }}m · {{ origin.climate }}</p>
      </div>

      <!-- Flavor Profile -->
      <!-- 上段: 左=フレーバーノート+品種・精製方法 / 右=レーダーチャート -->
      <div class="flex flex-col sm:flex-row gap-4 mb-6">

        <!-- 左カラム -->
        <div class="flex flex-col gap-4 flex-1">
          <!-- Flavor Notes -->
          <div class="bg-white rounded-2xl p-4 shadow-sm">
            <h2 class="text-base font-semibold text-coffee-600 mb-3">{{ t('detail.flavorNotes') }}</h2>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="note in origin.flavor_notes"
                :key="note"
                class="bg-coffee-100 text-coffee-600 text-xs px-3 py-1 rounded-full"
              >{{ note }}</span>
            </div>
          </div>

          <!-- Varieties / Process / Roast -->
          <div class="flex flex-col gap-4">
            <div class="bg-white rounded-xl p-4 shadow-sm">
              <p class="text-xs text-coffee-400 mb-1">{{ t('detail.varieties') }}</p>
              <p class="text-sm text-coffee-600">{{ origin.varieties.map(translateTerm).join(', ') || '—' }}</p>
            </div>
            <div class="bg-white rounded-xl p-4 shadow-sm">
              <p class="text-xs text-coffee-400 mb-1">{{ t('detail.processMethods') }}</p>
              <p class="text-sm text-coffee-600">{{ origin.process_methods.map(translateTerm).join(', ') || '—' }}</p>
            </div>
            <div v-if="origin.roast_levels?.length" class="bg-white rounded-xl p-4 shadow-sm">
              <p class="text-xs text-coffee-400 mb-2">{{ t('detail.roastLevel') }}</p>
              <div class="flex flex-wrap gap-1.5">
                <span
                  v-for="roast in origin.roast_levels"
                  :key="roast"
                  class="bg-amber-100 text-amber-700 text-xs px-3 py-1 rounded-full"
                >{{ translateTerm(roast) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 右カラム: レーダーチャート -->
        <div class="bg-white rounded-2xl p-2 shadow-sm flex flex-col items-center justify-center sm:w-1/2 flex-shrink-0 self-stretch">
          <h2 class="text-base font-semibold text-coffee-600 mb-1">{{ t('detail.flavorProfile') }}</h2>
          <FlavorRadar
            :acidity="origin.acidity"
            :bitterness="origin.bitterness"
            :sweetness="origin.sweetness"
            :body="origin.body"
            :show-values="true"
            class="w-full px-2"
          />
        </div>
      </div>

      <!-- 概要 -->
      <div class="prose prose-coffee max-w-none mb-8">
        <p class="text-coffee-600 leading-relaxed">
          {{ locale === 'ja' ? origin.description_ja : origin.description }}
        </p>
      </div>

      <!-- Back -->
      <RouterLink to="/origins" class="text-sm text-coffee-400 hover:text-coffee-600 transition-colors">
        {{ t('detail.back') }}
      </RouterLink>
    </template>
  </div>
</template>
