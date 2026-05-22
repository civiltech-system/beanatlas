<script setup lang="ts">
import type { Origin } from '@/types/origin'

defineProps<{ origin: Origin }>()
</script>

<template>
  <RouterLink
    :to="`/origins/${origin.slug}`"
    class="block bg-white rounded-2xl p-4 shadow-sm hover:shadow-md transition-all hover:-translate-y-0.5"
  >
    <p class="text-xs text-origin-green font-medium mb-1">{{ origin.region }}</p>
    <h3 class="text-lg font-serif font-bold text-coffee-600 mb-2">{{ origin.country }}</h3>
    <p class="text-xs text-coffee-400 mb-3">{{ origin.altitude_min }}–{{ origin.altitude_max }}m</p>
    <div class="flex flex-wrap gap-1">
      <span
        v-for="note in origin.flavor_notes.slice(0, 3)"
        :key="note"
        class="bg-coffee-100 text-coffee-500 text-xs px-2 py-0.5 rounded-full"
      >{{ note }}</span>
    </div>
  </RouterLink>
</template>
