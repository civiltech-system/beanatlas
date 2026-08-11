<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useOriginsStore } from '@/stores/origins'
import OriginCard from '@/components/OriginCard.vue'
import { useLocale } from '@/composables/useLocale'
import { useOriginFilter } from '@/composables/useOriginFilter'

const store = useOriginsStore()
const { locale, translateTerm } = useLocale()
const showSliders = ref(false)

onMounted(() => store.loadOrigins())

const {
  searchText, selectedContinent, selectedFlavors, selectedProcesses, selectedRoasts,
  flavorMin, sortKey,
  allContinents, groupedFlavorNotes, allProcessMethods, allRoastLevels,
  filtered, isFiltered, resetFilters, toggleFlavor, toggleProcess, toggleRoast,
} = useOriginFilter(() => store.origins)

const CONTINENT_ALL = { en: 'All', ja: 'すべて' }
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
    <h1 class="text-3xl font-serif font-bold text-coffee-600 mb-6">
      {{ locale === 'ja' ? 'コーヒー産地一覧' : 'Coffee Origins' }}
    </h1>

    <!-- Filter panel -->
    <div class="bg-white rounded-2xl shadow-sm p-5 mb-6 space-y-5">

      <!-- 1. テキスト検索 -->
      <input
        v-model="searchText"
        type="search"
        :placeholder="locale === 'ja' ? '国名・フレーバーで検索...' : 'Search by country or flavor...'"
        class="w-full px-4 py-2.5 rounded-xl bg-coffee-50 border border-coffee-100 text-coffee-600 placeholder:text-coffee-300 outline-none focus:ring-2 focus:ring-coffee-200 text-sm"
      />

      <!-- 2. 地域フィルター -->
      <div>
        <p class="text-xs font-semibold text-coffee-400 uppercase tracking-wide mb-2">
          {{ locale === 'ja' ? '地域' : 'Region' }}
        </p>
        <div class="flex flex-wrap gap-2">
          <button
            @click="selectedContinent = 'all'"
            :class="[
              selectedContinent === 'all'
                ? 'bg-coffee-600 text-white'
                : 'bg-coffee-50 text-coffee-500 border border-coffee-100 hover:bg-coffee-100',
              'px-3 py-1 rounded-full text-sm font-medium transition-colors'
            ]"
          >{{ locale === 'ja' ? CONTINENT_ALL.ja : CONTINENT_ALL.en }}</button>
          <button
            v-for="c in allContinents"
            :key="c"
            @click="selectedContinent = c"
            :class="[
              selectedContinent === c
                ? 'bg-coffee-600 text-white'
                : 'bg-coffee-50 text-coffee-500 border border-coffee-100 hover:bg-coffee-100',
              'px-3 py-1 rounded-full text-sm font-medium transition-colors'
            ]"
          >{{ translateTerm(c) }}</button>
        </div>
      </div>

      <!-- 3. フレーバーノート（カテゴリー別） -->
      <div>
        <p class="text-xs font-semibold text-coffee-400 uppercase tracking-wide mb-3">
          {{ locale === 'ja' ? 'フレーバーノート' : 'Flavor Notes' }}
        </p>
        <div class="space-y-3 max-h-40 overflow-y-auto pr-1">
          <div v-for="group in groupedFlavorNotes" :key="group.key">
            <p class="text-xs text-coffee-300 mb-1.5">
              {{ locale === 'ja' ? group.ja : group.en }}
            </p>
            <div class="flex flex-wrap gap-1.5">
              <button
                v-for="note in group.notes"
                :key="note"
                @click="toggleFlavor(note)"
                :class="[
                  selectedFlavors.includes(note)
                    ? 'bg-coffee-400 text-white'
                    : 'bg-coffee-50 text-coffee-500 border border-coffee-100 hover:bg-coffee-100',
                  'px-2.5 py-1 rounded-full text-xs transition-colors'
                ]"
              >{{ translateTerm(note) }}</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 4. 精製方法 -->
      <div>
        <p class="text-xs font-semibold text-coffee-400 uppercase tracking-wide mb-2">
          {{ locale === 'ja' ? '精製方法' : 'Process Method' }}
        </p>
        <div class="flex flex-wrap gap-1.5">
          <button
            v-for="proc in allProcessMethods"
            :key="proc"
            @click="toggleProcess(proc)"
            :class="[
              selectedProcesses.includes(proc)
                ? 'bg-origin-green text-white'
                : 'bg-coffee-50 text-coffee-500 border border-coffee-100 hover:bg-coffee-100',
              'px-2.5 py-1 rounded-full text-xs transition-colors'
            ]"
          >{{ translateTerm(proc) }}</button>
        </div>
      </div>

      <!-- 5. 焙煎度 -->
      <div v-if="allRoastLevels.length > 0">
        <p class="text-xs font-semibold text-coffee-400 uppercase tracking-wide mb-2">
          {{ locale === 'ja' ? '焙煎度' : 'Roast Level' }}
        </p>
        <div class="flex flex-wrap gap-1.5">
          <button
            v-for="roast in allRoastLevels"
            :key="roast"
            @click="toggleRoast(roast)"
            :class="[
              selectedRoasts.includes(roast)
                ? 'bg-amber-600 text-white'
                : 'bg-coffee-50 text-coffee-500 border border-coffee-100 hover:bg-coffee-100',
              'px-2.5 py-1 rounded-full text-xs transition-colors'
            ]"
          >{{ translateTerm(roast) }}</button>
        </div>
      </div>

      <!-- 6. フレーバー強度スライダー（折りたたみ） -->
      <div>
        <button
          @click="showSliders = !showSliders"
          class="flex items-center gap-1.5 text-xs font-semibold text-coffee-400 uppercase tracking-wide hover:text-coffee-600 transition-colors"
        >
          <span>{{ locale === 'ja' ? 'フレーバー強度で絞り込む' : 'Filter by Intensity' }}</span>
          <span>{{ showSliders ? '▲' : '▼' }}</span>
        </button>
        <div v-if="showSliders" class="grid grid-cols-2 md:grid-cols-4 gap-5 mt-4">
          <div v-for="key in (['acidity', 'bitterness', 'sweetness', 'body'] as const)" :key="key">
            <div class="flex justify-between text-xs text-coffee-400 mb-1">
              <span>{{
                locale === 'ja'
                  ? { acidity: '酸味', bitterness: '苦味', sweetness: '甘味', body: 'コク' }[key]
                  : { acidity: 'Acidity', bitterness: 'Bitterness', sweetness: 'Sweetness', body: 'Body' }[key]
              }}</span>
              <span class="font-medium text-coffee-500">
                {{ flavorMin[key] > 0
                  ? (locale === 'ja' ? `${flavorMin[key]} 以上` : `≥ ${flavorMin[key]}`)
                  : (locale === 'ja' ? '指定なし' : 'Any')
                }}
              </span>
            </div>
            <input
              type="range"
              min="0"
              max="5"
              step="1"
              v-model.number="flavorMin[key]"
              class="w-full accent-coffee-400"
            />
            <div class="flex justify-between text-xs text-coffee-200 mt-0.5">
              <span>0</span><span>5</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 結果バー -->
    <div class="flex items-center justify-between mb-5">
      <p class="text-sm text-coffee-400">
        {{ filtered.length }}{{ locale === 'ja' ? ' 件の産地' : ' origins' }}
      </p>
      <div class="flex items-center gap-3">
        <!-- 6. ソート -->
        <select
          v-model="sortKey"
          class="text-sm text-coffee-600 bg-white border border-coffee-100 rounded-lg px-3 py-1.5 outline-none focus:ring-2 focus:ring-coffee-200 cursor-pointer"
        >
          <option value="default">{{ locale === 'ja' ? '並び替え' : 'Sort by' }}</option>
          <option value="acidity">{{ locale === 'ja' ? '酸味が強い順' : 'Highest Acidity' }}</option>
          <option value="bitterness">{{ locale === 'ja' ? '苦味が強い順' : 'Highest Bitterness' }}</option>
          <option value="sweetness">{{ locale === 'ja' ? '甘味が強い順' : 'Highest Sweetness' }}</option>
          <option value="body">{{ locale === 'ja' ? 'コクが強い順' : 'Highest Body' }}</option>
          <option value="altitude">{{ locale === 'ja' ? '標高が高い順' : 'Highest Altitude' }}</option>
        </select>
        <button
          v-if="isFiltered"
          @click="resetFilters"
          class="text-sm text-coffee-400 hover:text-coffee-600 transition-colors underline underline-offset-2"
        >{{ locale === 'ja' ? 'リセット' : 'Reset' }}</button>
      </div>
    </div>

    <!-- グリッド -->
    <div v-if="store.loading" class="text-coffee-400 text-center py-12">
      {{ locale === 'ja' ? '読み込み中...' : 'Loading...' }}
    </div>
    <div v-else-if="store.error" class="text-red-500 text-center py-12">{{ store.error }}</div>
    <div v-else-if="filtered.length === 0" class="text-coffee-400 text-center py-16">
      <p class="text-lg mb-2">
        {{ locale === 'ja' ? '条件に合う産地が見つかりません' : 'No origins match your filters.' }}
      </p>
      <button @click="resetFilters" class="text-sm text-coffee-400 underline underline-offset-2 hover:text-coffee-600">
        {{ locale === 'ja' ? 'フィルターをリセット' : 'Reset filters' }}
      </button>
    </div>
    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <OriginCard v-for="origin in filtered" :key="origin.id" :origin="origin" />
    </div>
  </div>
</template>
