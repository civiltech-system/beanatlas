<script setup lang="ts">
import type { Origin } from '@/types/origin'
import { useLocale } from '@/composables/useLocale'

defineProps<{ origin: Origin }>()
const { locale, translateTerm } = useLocale()
</script>

<template>
  <RouterLink
    :to="`/origins/${origin.slug}`"
    class="block bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition-all hover:-translate-y-0.5"
  >
    <p class="text-xs text-origin-green font-medium mb-1">
      {{ origin.region }}
      <span v-if="origin.sub_region" class="text-coffee-300"> › {{ origin.sub_region }}</span>
    </p>
    <h3 class="text-lg font-serif font-bold text-coffee-600 mb-2">
      {{ locale === 'ja' ? origin.country_ja : origin.country }}
    </h3>
    <p class="text-xs text-coffee-400 mb-2">{{ origin.altitude_min }}–{{ origin.altitude_max }}m</p>
    <div v-if="origin.roast_levels?.length" class="flex flex-wrap gap-1 mb-2">
      <span
        v-for="roast in origin.roast_levels"
        :key="roast"
        class="bg-amber-50 text-amber-600 text-xs px-2 py-0.5 rounded-full"
      >{{ translateTerm(roast) }}</span>
    </div>
    <div class="flex flex-wrap gap-1">
      <span
        v-for="note in origin.flavor_notes.slice(0, 3)"
        :key="note"
        class="bg-coffee-100 text-coffee-500 text-xs px-2 py-0.5 rounded-full"
      >{{ note }}</span>
    </div>
  </RouterLink>
</template>
