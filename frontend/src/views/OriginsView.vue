<script setup lang="ts">
import { onMounted } from 'vue'
import { useOriginsStore } from '@/stores/origins'
import OriginCard from '@/components/OriginCard.vue'
import { usePageMeta } from '@/composables/usePageMeta'
import { useLocale } from '@/composables/useLocale'
import { useOriginFilter, type SortKey } from '@/composables/useOriginFilter'

const store = useOriginsStore()
const { locale, t, translateTerm } = useLocale()

const {
  searchText, selectedContinent, selectedFlavors, selectedProcesses, selectedRoasts,
  sortKey, allContinents, groupedFlavorNotes, allProcessMethods, allRoastLevels,
  filtered, isFiltered, resetFilters, toggleFlavor, toggleProcess, toggleRoast,
} = useOriginFilter(() => store.origins)

onMounted(() => store.loadOrigins())

usePageMeta({
  title: 'コーヒー産地一覧 - 品種・精製方法から探す',
  description:
    '世界各国のコーヒー産地を品種・精製方法・フレーバー・焙煎度で絞り込んで比較。標高や地域ごとの特徴も一覧で確認できます。',
  path: '/origins',
})

const sortOptions: { value: SortKey; labelKey: 'sortDefault' | 'altitude' }[] = [
  { value: 'default', labelKey: 'sortDefault' },
  { value: 'altitude', labelKey: 'altitude' },
]

function chipClass(active: boolean) {
  return active
    ? 'bg-coffee-600 text-white'
    : 'bg-white text-coffee-500 hover:bg-coffee-100'
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-6 py-12">
    <h1 class="text-3xl font-serif font-bold text-coffee-600 mb-2">{{ t('origins.title') }}</h1>
    <p class="text-coffee-400 text-sm mb-6">
      {{ locale === 'ja'
        ? '品種・精製方法・フレーバーで絞り込んで、世界のコーヒー産地を比較できます。'
        : 'Filter by variety, process method, and flavor to compare coffee origins worldwide.' }}
    </p>

    <!-- 検索 & 並び替え -->
    <div class="flex flex-col sm:flex-row gap-3 mb-4">
      <div class="flex items-center bg-white rounded-xl shadow-sm px-3 py-2 gap-2 flex-1">
        <svg class="w-4 h-4 text-coffee-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11A6 6 0 1 1 5 11a6 6 0 0 1 12 0z"/>
        </svg>
        <input
          v-model="searchText"
          type="text"
          :placeholder="t('filter.searchPlaceholder')"
          class="flex-1 text-sm text-coffee-600 placeholder:text-coffee-300 outline-none bg-transparent"
        />
      </div>
      <select
        v-model="sortKey"
        class="bg-white rounded-xl shadow-sm px-3 py-2 text-sm text-coffee-600 outline-none"
      >
        <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
          {{ t('filter.sort') }}: {{ t(`filter.${opt.labelKey}`) }}
        </option>
      </select>
    </div>

    <!-- 地域フィルター -->
    <div class="flex flex-wrap items-center gap-1.5 mb-3">
      <span class="text-xs text-coffee-400 mr-1">{{ t('filter.region') }}</span>
      <button
        class="text-xs px-2.5 py-1 rounded-full transition-colors"
        :class="chipClass(selectedContinent === 'all')"
        @click="selectedContinent = 'all'"
      >{{ t('filter.all') }}</button>
      <button
        v-for="continent in allContinents"
        :key="continent"
        class="text-xs px-2.5 py-1 rounded-full transition-colors"
        :class="chipClass(selectedContinent === continent)"
        @click="selectedContinent = continent"
      >{{ translateTerm(continent) }}</button>
    </div>

    <!-- フレーバーフィルター -->
    <div v-for="group in groupedFlavorNotes" :key="group.key" class="flex flex-wrap items-center gap-1.5 mb-2">
      <span class="text-xs text-coffee-400 mr-1 w-20 flex-shrink-0">{{ locale === 'ja' ? group.ja : group.en }}</span>
      <button
        v-for="note in group.notes"
        :key="note"
        class="text-xs px-2.5 py-1 rounded-full transition-colors"
        :class="chipClass(selectedFlavors.includes(note))"
        @click="toggleFlavor(note)"
      >{{ translateTerm(note) }}</button>
    </div>

    <!-- 精製方法・焙煎度フィルター -->
    <div class="flex flex-wrap items-center gap-1.5 mb-2">
      <span class="text-xs text-coffee-400 mr-1 w-20 flex-shrink-0">{{ t('filter.process') }}</span>
      <button
        v-for="method in allProcessMethods"
        :key="method"
        class="text-xs px-2.5 py-1 rounded-full transition-colors"
        :class="chipClass(selectedProcesses.includes(method))"
        @click="toggleProcess(method)"
      >{{ translateTerm(method) }}</button>
    </div>
    <div class="flex flex-wrap items-center gap-1.5 mb-4">
      <span class="text-xs text-coffee-400 mr-1 w-20 flex-shrink-0">{{ t('filter.roast') }}</span>
      <button
        v-for="roast in allRoastLevels"
        :key="roast"
        class="text-xs px-2.5 py-1 rounded-full transition-colors"
        :class="chipClass(selectedRoasts.includes(roast))"
        @click="toggleRoast(roast)"
      >{{ translateTerm(roast) }}</button>
    </div>

    <div class="flex items-center justify-between mb-6">
      <p class="text-sm text-coffee-400">{{ filtered.length }}{{ t('filter.resultsSuffix') }}</p>
      <button
        v-if="isFiltered"
        class="text-sm text-coffee-500 underline hover:text-coffee-600"
        @click="resetFilters"
      >{{ t('filter.reset') }}</button>
    </div>

    <div v-if="store.loading" class="text-coffee-400 text-center py-12">{{ t('origins.loading') }}</div>
    <div v-else-if="store.error" class="text-red-500 text-center py-12">{{ store.error }}</div>
    <div v-else-if="filtered.length === 0" class="text-coffee-400 text-center py-12">{{ t('filter.noResults') }}</div>
    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <OriginCard v-for="origin in filtered" :key="origin.id" :origin="origin" />
    </div>
  </div>
</template>
