<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import MapView from '@/components/MapView.vue'
import FlavorIndicator from '@/components/FlavorIndicator.vue'
import FlavorRadar from '@/components/FlavorRadar.vue'
import { usePageMeta } from '@/composables/usePageMeta'
import type { Origin } from '@/types/origin'
import { useLocale } from '@/composables/useLocale'
import { useOriginsStore } from '@/stores/origins'

const selected = ref<Origin | null>(null)
const { locale, t, translateTerm } = useLocale()
const store = useOriginsStore()
const mapRef = ref<InstanceType<typeof MapView> | null>(null)

const searchQuery = ref('')
const showDropdown = ref(false)

onMounted(() => store.loadOrigins())

usePageMeta({
  title: 'コーヒー産地マップ - 世界のコーヒー生産地を探る',
  description:
    '世界のコーヒー産地をインタラクティブな地図で探索。産地ごとのフレーバー、品種、精製方法、標高などのデータを一目で確認できます。',
  path: '/',
})

function onSelect(origin: Origin) {
  selected.value = origin
  searchQuery.value = ''
  showDropdown.value = false
}

function closePanel() {
  selected.value = null
}

const searchResults = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return []
  return store.origins
    .filter(o =>
      o.country.toLowerCase().includes(q) ||
      o.country_ja.includes(q) ||
      o.region.toLowerCase().includes(q),
    )
    .slice(0, 6)
})

function selectFromSearch(origin: Origin) {
  mapRef.value?.flyToOrigin(origin)
  selected.value = origin
  searchQuery.value = ''
  showDropdown.value = false
}

function onSearchFocus() {
  showDropdown.value = true
}

function onSearchBlur() {
  // 少し遅らせてクリックイベントを先に処理させる
  setTimeout(() => { showDropdown.value = false }, 150)
}
</script>

<template>
  <!-- 全画面マップ（ヘッダー 56px 分を引く） -->
  <div class="relative" style="height: calc(100vh - 56px);">

    <!-- マップ -->
    <MapView ref="mapRef" class="absolute inset-0" @select="onSelect" />

    <!-- 7. マップ検索ボックス -->
    <div class="absolute top-3 left-3 z-10 w-64">
      <div class="relative">
        <div class="flex items-center bg-white rounded-xl shadow-md px-3 py-2 gap-2">
          <svg class="w-4 h-4 text-coffee-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="産地を検索..."
            class="flex-1 text-sm text-coffee-600 placeholder:text-coffee-300 outline-none bg-transparent"
            @focus="onSearchFocus"
            @blur="onSearchBlur"
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="text-coffee-300 hover:text-coffee-500 transition-colors text-base leading-none"
          >✕</button>
        </div>

        <!-- 検索結果ドロップダウン -->
        <div
          v-if="showDropdown && searchResults.length > 0"
          class="absolute top-full left-0 right-0 mt-1 bg-white rounded-xl shadow-lg overflow-hidden"
        >
          <button
            v-for="origin in searchResults"
            :key="origin.id"
            @mousedown.prevent="selectFromSearch(origin)"
            class="w-full text-left px-4 py-2.5 hover:bg-coffee-50 transition-colors border-b border-coffee-50 last:border-0"
          >
            <p class="text-sm font-medium text-coffee-600">
              {{ locale === 'ja' ? origin.country_ja : origin.country }}
            </p>
            <p class="text-xs text-coffee-400">{{ origin.region }}</p>
          </button>
        </div>
      </div>
    </div>

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
          <h2 class="text-2xl font-serif font-bold">
            {{ locale === 'ja' ? selected.country_ja : selected.country }}
          </h2>
          <p class="text-coffee-300 text-sm mt-1">{{ selected.altitude_min }}–{{ selected.altitude_max }}m · {{ selected.climate }}</p>
        </div>

        <!-- 本文 -->
        <div class="px-5 py-5 flex flex-col gap-5 flex-1">

          <!-- フレーバーノート -->
          <div>
            <p class="text-xs font-semibold text-coffee-400 uppercase tracking-wide mb-2">{{ t('panel.flavorNotes') }}</p>
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
            <p class="text-xs font-semibold text-coffee-400 uppercase tracking-wide mb-3">{{ t('panel.flavorProfile') }}</p>
            <FlavorRadar
              :acidity="selected.acidity"
              :bitterness="selected.bitterness"
              :sweetness="selected.sweetness"
              :body="selected.body"
              class="mb-3 px-4"
            />
            <div class="space-y-2.5">
              <FlavorIndicator :label="t('flavor.acidity')" :value="selected.acidity" />
              <FlavorIndicator :label="t('flavor.bitterness')" :value="selected.bitterness" />
              <FlavorIndicator :label="t('flavor.sweetness')" :value="selected.sweetness" />
              <FlavorIndicator :label="t('flavor.body')" :value="selected.body" />
            </div>
          </div>

          <!-- 基本情報 -->
          <div class="grid grid-cols-2 gap-2">
            <div class="bg-white rounded-xl p-3">
              <p class="text-xs text-coffee-400 mb-1">{{ t('panel.varieties') }}</p>
              <p class="text-xs text-coffee-600 font-medium">{{ selected.varieties.map(translateTerm).join(', ') || '—' }}</p>
            </div>
            <div class="bg-white rounded-xl p-3">
              <p class="text-xs text-coffee-400 mb-1">{{ t('panel.process') }}</p>
              <p class="text-xs text-coffee-600 font-medium">{{ selected.process_methods.map(translateTerm).join(', ') || '—' }}</p>
            </div>
          </div>

          <!-- 説明 -->
          <p class="text-sm text-coffee-600 leading-relaxed">
            {{ locale === 'ja' ? selected.description_ja : selected.description }}
          </p>

          <!-- 詳細ページリンク -->
          <RouterLink
            :to="`/origins/${selected.slug}`"
            class="mt-auto block text-center bg-coffee-600 text-white py-2.5 rounded-full text-sm font-medium hover:bg-coffee-500 transition-colors"
          >
            {{ t('panel.viewFull') }}
          </RouterLink>
        </div>
      </aside>
    </Transition>

  </div>
</template>
