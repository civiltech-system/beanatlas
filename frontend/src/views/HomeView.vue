<script setup lang="ts">
import { ref } from 'vue'
import MapView from '@/components/MapView.vue'
import FlavorIndicator from '@/components/FlavorIndicator.vue'
import FlavorRadar from '@/components/FlavorRadar.vue'
import type { Origin } from '@/types/origin'

const selected = ref<Origin | null>(null)

function onSelect(origin: Origin) {
  selected.value = origin
}

function closePanel() {
  selected.value = null
}
</script>

<template>
  <!-- 全画面マップ（ヘッダー 56px 分を引く） -->
  <div class="relative" style="height: calc(100vh - 56px);">

    <!-- マップ -->
    <MapView class="absolute inset-0" @select="onSelect" />

    <!-- 左パネル -->
    <Transition
      enter-active-class="transition-transform duration-300 ease-out"
      enter-from-class="-translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition-transform duration-200 ease-in"
      leave-from-class="translate-x-0"
      leave-to-class="-translate-x-full"
    >
      <aside
        v-if="selected"
        class="absolute top-0 left-0 h-full w-80 bg-coffee-50 shadow-2xl overflow-y-auto z-10 flex flex-col"
      >
        <!-- ヘッダー -->
        <div class="bg-coffee-600 text-coffee-50 px-5 pt-5 pb-6 flex-shrink-0">
          <div class="flex items-start justify-between gap-2 mb-1">
            <p class="text-xs text-coffee-300 font-medium">{{ selected.region }}</p>
            <button
              @click="closePanel"
              class="text-coffee-300 hover:text-white transition-colors text-lg leading-none mt-0.5 flex-shrink-0"
              aria-label="Close"
            >✕</button>
          </div>
          <h2 class="text-2xl font-serif font-bold">{{ selected.country }}</h2>
          <p class="text-coffee-300 text-sm mt-1">{{ selected.altitude_min }}–{{ selected.altitude_max }}m · {{ selected.climate }}</p>
        </div>

        <!-- 本文 -->
        <div class="px-5 py-5 flex flex-col gap-5 flex-1">

          <!-- フレーバーノート -->
          <div>
            <p class="text-xs font-semibold text-coffee-400 uppercase tracking-wide mb-2">Flavor Notes</p>
            <div class="flex flex-wrap gap-1.5">
              <span
                v-for="note in selected.flavor_notes"
                :key="note"
                class="bg-coffee-100 text-coffee-600 text-xs px-2.5 py-1 rounded-full"
              >{{ note }}</span>
            </div>
          </div>

          <!-- フレーバープロファイル -->
          <div>
            <p class="text-xs font-semibold text-coffee-400 uppercase tracking-wide mb-3">Flavor Profile</p>
            <FlavorRadar
              :acidity="selected.acidity"
              :bitterness="selected.bitterness"
              :sweetness="selected.sweetness"
              :body="selected.body"
              class="mb-3 px-4"
            />
            <div class="space-y-2.5">
              <FlavorIndicator label="Acidity" :value="selected.acidity" />
              <FlavorIndicator label="Bitterness" :value="selected.bitterness" />
              <FlavorIndicator label="Sweetness" :value="selected.sweetness" />
              <FlavorIndicator label="Body" :value="selected.body" />
            </div>
          </div>

          <!-- 基本情報 -->
          <div class="grid grid-cols-2 gap-2">
            <div class="bg-white rounded-xl p-3">
              <p class="text-xs text-coffee-400 mb-1">Varieties</p>
              <p class="text-xs text-coffee-600 font-medium">{{ selected.varieties.join(', ') || '—' }}</p>
            </div>
            <div class="bg-white rounded-xl p-3">
              <p class="text-xs text-coffee-400 mb-1">Process</p>
              <p class="text-xs text-coffee-600 font-medium">{{ selected.process_methods.join(', ') || '—' }}</p>
            </div>
          </div>

          <!-- 説明 -->
          <p class="text-sm text-coffee-600 leading-relaxed">{{ selected.description }}</p>

          <!-- 詳細ページリンク -->
          <RouterLink
            :to="`/origins/${selected.slug}`"
            class="mt-auto block text-center bg-coffee-600 text-white py-2.5 rounded-full text-sm font-medium hover:bg-coffee-500 transition-colors"
          >
            View Full Profile →
          </RouterLink>
        </div>
      </aside>
    </Transition>

  </div>
</template>
