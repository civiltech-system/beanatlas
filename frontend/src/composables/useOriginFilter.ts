import { ref, computed } from 'vue'
import type { Origin } from '@/types/origin'

export type SortKey = 'default' | 'acidity' | 'bitterness' | 'sweetness' | 'body' | 'altitude'

const CONTINENT: Record<string, string> = {
  ethiopia: 'Africa', kenya: 'Africa', tanzania: 'Africa', rwanda: 'Africa', burundi: 'Africa',
  colombia: 'Americas', brazil: 'Americas', guatemala: 'Americas', 'costa-rica': 'Americas',
  mexico: 'Americas', honduras: 'Americas', 'el-salvador': 'Americas', peru: 'Americas',
  bolivia: 'Americas', jamaica: 'Americas',
  indonesia: 'Asia & Pacific', vietnam: 'Asia & Pacific', india: 'Asia & Pacific',
  'papua-new-guinea': 'Asia & Pacific', yemen: 'Asia & Pacific',
}

export function getContinent(origin: Origin): string {
  return CONTINENT[origin.slug] ?? 'Other'
}

export interface FlavorGroup {
  key: string
  en: string
  ja: string
  notes: string[]
}

export const FLAVOR_GROUPS: FlavorGroup[] = [
  {
    key: 'fruit',
    en: 'Fruit',
    ja: 'フルーツ系',
    notes: ['Blueberry', 'Citrus', 'Red Apple', 'Berry', 'Apricot', 'Blackcurrant', 'Grapefruit',
      'Wild Berry', 'Dried Fruit', 'Peach', 'Mild Citrus', 'Plum', 'Raspberry', 'Green Apple',
      'Stone Fruit', 'Fruity', 'Tropical'],
  },
  {
    key: 'sweet',
    en: 'Sweet & Chocolate',
    ja: 'スイート・チョコ',
    notes: ['Caramel', 'Chocolate', 'Dark Chocolate', 'Milk Chocolate', 'Brown Sugar', 'Honey',
      'Toffee', 'Vanilla', 'Creamy'],
  },
  {
    key: 'floral',
    en: 'Floral',
    ja: 'フラワー系',
    notes: ['Jasmine', 'Floral', 'Hibiscus'],
  },
  {
    key: 'earthy',
    en: 'Earthy & Spice',
    ja: 'アース・スパイス',
    notes: ['Spice', 'Earthy', 'Cedar', 'Tobacco', 'Wild', 'Rubbery', 'Woody'],
  },
  {
    key: 'tea',
    en: 'Tea & Wine',
    ja: 'お茶・ワイン',
    notes: ['Black Tea', 'Wine-like'],
  },
  {
    key: 'other',
    en: 'Other',
    ja: 'その他',
    notes: ['Nutty', 'Nuts', 'Low Acidity', 'Tomato', 'Strong Bitter', 'Mild', 'Mild Acidity', 'No Bitterness'],
  },
]

const ROAST_ORDER = ['Light', 'Medium-Light', 'Medium', 'Medium-Dark', 'Dark']

export function useOriginFilter(originsGetter: () => Origin[]) {
  const searchText = ref('')
  const selectedContinent = ref('all')
  const selectedFlavors = ref<string[]>([])
  const selectedProcesses = ref<string[]>([])
  const selectedRoasts = ref<string[]>([])
  const flavorMin = ref({ acidity: 0, bitterness: 0, sweetness: 0, body: 0 })
  const sortKey = ref<SortKey>('default')

  const allContinents = computed(() => {
    const set = new Set(originsGetter().map(o => getContinent(o)))
    return Array.from(set).sort()
  })

  // データに存在するノートだけを含む、カテゴリー別グループ
  const groupedFlavorNotes = computed(() => {
    const existing = new Set(originsGetter().flatMap(o => o.flavor_notes))
    return FLAVOR_GROUPS
      .map(g => ({ ...g, notes: g.notes.filter(n => existing.has(n)) }))
      .filter(g => g.notes.length > 0)
  })

  const allFlavorNotes = computed(() =>
    groupedFlavorNotes.value.flatMap(g => g.notes),
  )

  const allProcessMethods = computed(() => {
    const set = new Set(originsGetter().flatMap(o => o.process_methods))
    return Array.from(set).sort()
  })

  const allRoastLevels = computed(() => {
    const set = new Set(originsGetter().flatMap(o => o.roast_levels ?? []))
    return ROAST_ORDER.filter(r => set.has(r))
  })

  const filtered = computed(() => {
    let result = originsGetter()

    const q = searchText.value.trim().toLowerCase()
    if (q) {
      result = result.filter(o =>
        o.country.toLowerCase().includes(q) ||
        o.country_ja.includes(q) ||
        o.region.toLowerCase().includes(q) ||
        (o.sub_region?.toLowerCase().includes(q) ?? false) ||
        (o.farm?.toLowerCase().includes(q) ?? false) ||
        o.flavor_notes.some(n => n.toLowerCase().includes(q)),
      )
    }

    if (selectedContinent.value !== 'all') {
      result = result.filter(o => getContinent(o) === selectedContinent.value)
    }

    if (selectedFlavors.value.length > 0) {
      result = result.filter(o =>
        selectedFlavors.value.some(f => o.flavor_notes.includes(f)),
      )
    }

    if (selectedProcesses.value.length > 0) {
      result = result.filter(o =>
        selectedProcesses.value.some(p => o.process_methods.includes(p)),
      )
    }

    if (selectedRoasts.value.length > 0) {
      result = result.filter(o =>
        selectedRoasts.value.some(r => (o.roast_levels ?? []).includes(r)),
      )
    }

    const m = flavorMin.value
    if (m.acidity > 0 || m.bitterness > 0 || m.sweetness > 0 || m.body > 0) {
      result = result.filter(o =>
        o.acidity >= m.acidity &&
        o.bitterness >= m.bitterness &&
        o.sweetness >= m.sweetness &&
        o.body >= m.body,
      )
    }

    if (sortKey.value !== 'default') {
      result = [...result].sort((a, b) => {
        const va = sortKey.value === 'altitude' ? a.altitude_max : (a[sortKey.value as keyof Origin] as number)
        const vb = sortKey.value === 'altitude' ? b.altitude_max : (b[sortKey.value as keyof Origin] as number)
        return vb - va
      })
    }

    return result
  })

  const isFiltered = computed(() =>
    searchText.value !== '' ||
    selectedContinent.value !== 'all' ||
    selectedFlavors.value.length > 0 ||
    selectedProcesses.value.length > 0 ||
    selectedRoasts.value.length > 0 ||
    flavorMin.value.acidity > 0 || flavorMin.value.bitterness > 0 ||
    flavorMin.value.sweetness > 0 || flavorMin.value.body > 0 ||
    sortKey.value !== 'default',
  )

  function resetFilters() {
    searchText.value = ''
    selectedContinent.value = 'all'
    selectedFlavors.value = []
    selectedProcesses.value = []
    selectedRoasts.value = []
    flavorMin.value = { acidity: 0, bitterness: 0, sweetness: 0, body: 0 }
    sortKey.value = 'default'
  }

  function toggleFlavor(note: string) {
    const idx = selectedFlavors.value.indexOf(note)
    if (idx === -1) selectedFlavors.value.push(note)
    else selectedFlavors.value.splice(idx, 1)
  }

  function toggleProcess(method: string) {
    const idx = selectedProcesses.value.indexOf(method)
    if (idx === -1) selectedProcesses.value.push(method)
    else selectedProcesses.value.splice(idx, 1)
  }

  function toggleRoast(roast: string) {
    const idx = selectedRoasts.value.indexOf(roast)
    if (idx === -1) selectedRoasts.value.push(roast)
    else selectedRoasts.value.splice(idx, 1)
  }

  return {
    searchText, selectedContinent, selectedFlavors, selectedProcesses, selectedRoasts,
    flavorMin, sortKey,
    allContinents, groupedFlavorNotes, allFlavorNotes, allProcessMethods, allRoastLevels,
    filtered, isFiltered, resetFilters, toggleFlavor, toggleProcess, toggleRoast,
  }
}
