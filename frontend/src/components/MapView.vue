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

  await store.loadOrigins()
  addMarkers()
})

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
