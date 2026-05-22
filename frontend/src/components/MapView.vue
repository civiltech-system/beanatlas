<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import maplibregl from 'maplibre-gl'
import { useOriginsStore } from '@/stores/origins'
import type { Origin } from '@/types/origin'

const emit = defineEmits<{ select: [origin: Origin] }>()

const container = ref<HTMLDivElement | null>(null)
const store = useOriginsStore()
let map: maplibregl.Map | null = null
const markers: maplibregl.Marker[] = []

onMounted(async () => {
  if (!container.value) return

  map = new maplibregl.Map({
    container: container.value,
    style: 'https://tiles.openfreemap.org/styles/liberty',
    center: [20, 10],
    zoom: 1.8,
    dragRotate: false,
    touchZoomRotate: false,
  })

  map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right')

  // スタイル読み込みとデータ取得を並行して待つ
  await Promise.all([
    store.loadOrigins(),
    new Promise<void>(resolve => map!.on('load', resolve)),
  ])

  try {
    customizeLabels()
  } catch (e) {
    console.warn('[MapView] customizeLabels failed:', e)
  }
  addMarkers()
})

function customizeLabels() {
  if (!map) return

  // ベースマップの place / poi ラベルをすべて非表示
  for (const layer of map.getStyle().layers) {
    if (layer.type !== 'symbol') continue
    const sourceLayer = (layer as any)['source-layer']
    if (sourceLayer === 'place' || sourceLayer === 'poi' || sourceLayer === 'housenumber') {
      map.setLayoutProperty(layer.id, 'visibility', 'none')
    }
  }

  // 残る道路名などを英語（name:en）に統一
  for (const layer of map.getStyle().layers) {
    if (layer.type !== 'symbol') continue
    const layout = (layer.layout ?? {}) as Record<string, unknown>
    if ('text-field' in layout) {
      map.setLayoutProperty(layer.id, 'text-field', [
        'coalesce',
        ['get', 'name:en'],
        ['get', 'name'],
      ])
    }
  }

  // データがある国だけを独自ラベルで表示
  map.addSource('origin-country-labels', {
    type: 'geojson',
    data: {
      type: 'FeatureCollection',
      features: store.origins.map(o => ({
        type: 'Feature',
        geometry: { type: 'Point', coordinates: [o.longitude, o.latitude] },
        properties: { name: o.country },
      })),
    },
  })

  map.addLayer({
    id: 'origin-country-label',
    type: 'symbol',
    source: 'origin-country-labels',
    layout: {
      'text-field': ['get', 'name'],
      'text-size': ['interpolate', ['linear'], ['zoom'], 1, 10, 5, 14],
      'text-font': ['Open Sans Bold', 'Arial Unicode MS Bold'],
      'text-anchor': 'top',
      'text-offset': [0, 1.5],
      'text-allow-overlap': false,
    },
    paint: {
      'text-color': '#1a3a5c',
      'text-halo-color': 'rgba(255,255,255,0.85)',
      'text-halo-width': 1.5,
    },
  })
}

function addMarkers() {
  if (!map) return

  for (const origin of store.origins) {
    // アウターリング（ホバー用の広いヒット領域）
    const wrapper = document.createElement('div')
    wrapper.style.cssText = `
      width: 28px; height: 28px;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer;
    `

    // 内側の見た目ドット
    const dot = document.createElement('div')
    dot.style.cssText = `
      width: 12px; height: 12px;
      background: #4A7C59;
      border: 2px solid white;
      border-radius: 50%;
      box-shadow: 0 1px 4px rgba(0,0,0,0.35);
      transition: background 0.15s, box-shadow 0.15s, width 0.15s, height 0.15s;
      pointer-events: none;
    `

    wrapper.appendChild(dot)

    // ホバー：ドットのサイズをwrapperのpadding内で変えるのでwrapper自体は動かない
    wrapper.addEventListener('mouseenter', () => {
      dot.style.width = '18px'
      dot.style.height = '18px'
      dot.style.background = '#C8813A'
      dot.style.boxShadow = '0 2px 8px rgba(0,0,0,0.4)'
    })
    wrapper.addEventListener('mouseleave', () => {
      dot.style.width = '12px'
      dot.style.height = '12px'
      dot.style.background = '#4A7C59'
      dot.style.boxShadow = '0 1px 4px rgba(0,0,0,0.35)'
    })

    wrapper.addEventListener('click', (e) => {
      e.stopPropagation()
      emit('select', origin)
    })

    const marker = new maplibregl.Marker({ element: wrapper, anchor: 'center' })
      .setLngLat([origin.longitude, origin.latitude])
      .addTo(map!)

    markers.push(marker)
  }
}

onUnmounted(() => {
  markers.forEach(m => m.remove())
  map?.remove()
})
</script>

<template>
  <div ref="container" class="w-full h-full" />
</template>
