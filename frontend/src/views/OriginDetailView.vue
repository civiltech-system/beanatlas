<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { Origin } from '@/types/origin'
import { fetchOrigin } from '@/api/origins'
import FlavorIndicator from '@/components/FlavorIndicator.vue'
import FlavorRadar from '@/components/FlavorRadar.vue'

const route = useRoute()
const origin = ref<Origin | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

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

      <!-- Back -->
      <RouterLink to="/origins" class="text-sm text-coffee-400 hover:text-coffee-600 transition-colors">
        ← Back to Origins
      </RouterLink>
    </template>
  </div>
</template>
