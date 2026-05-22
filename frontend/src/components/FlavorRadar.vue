<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  acidity: number
  bitterness: number
  sweetness: number
  body: number
}>()

const cx = 80
const cy = 80
const R = 52

const axes = [
  { label: 'Acidity' },
  { label: 'Bitterness' },
  { label: 'Sweetness' },
  { label: 'Body' },
]

const values = computed(() => [props.acidity, props.bitterness, props.sweetness, props.body])

function angle(i: number) {
  return (i * 2 * Math.PI) / 4 - Math.PI / 2
}

function point(i: number, ratio: number) {
  const a = angle(i)
  return { x: cx + ratio * R * Math.cos(a), y: cy + ratio * R * Math.sin(a) }
}

function polygonPoints(ratio: number) {
  return [0, 1, 2, 3].map(i => { const p = point(i, ratio); return `${p.x},${p.y}` }).join(' ')
}

const dataPolygon = computed(() =>
  values.value.map((v, i) => { const p = point(i, v / 5); return `${p.x},${p.y}` }).join(' ')
)

const labelR = R + 17
const labelConfig = [
  { anchor: 'middle', baseline: 'auto',    dy: -4 },
  { anchor: 'start',  baseline: 'middle',  dy: 0  },
  { anchor: 'middle', baseline: 'hanging', dy: 4  },
  { anchor: 'end',    baseline: 'middle',  dy: 0  },
]
</script>

<template>
  <svg viewBox="0 0 160 160" class="w-full" style="overflow: visible">
    <!-- Grid rings -->
    <polygon
      v-for="level in [1, 2, 3, 4, 5]"
      :key="level"
      :points="polygonPoints(level / 5)"
      fill="none"
      stroke="#D4B896"
      :stroke-width="level === 5 ? 0.8 : 0.5"
    />
    <!-- Axes -->
    <line
      v-for="(_, i) in 4"
      :key="i"
      :x1="cx" :y1="cy"
      :x2="point(i, 1).x" :y2="point(i, 1).y"
      stroke="#D4B896"
      stroke-width="0.5"
    />
    <!-- Data polygon -->
    <polygon
      :points="dataPolygon"
      fill="#4A7C59"
      fill-opacity="0.22"
      stroke="#4A7C59"
      stroke-width="1.5"
      stroke-linejoin="round"
    />
    <!-- Data dots -->
    <circle
      v-for="(v, i) in values"
      :key="i"
      :cx="point(i, v / 5).x"
      :cy="point(i, v / 5).y"
      r="3"
      fill="#4A7C59"
    />
    <!-- Labels -->
    <text
      v-for="(axis, i) in axes"
      :key="axis.label"
      :x="point(i, labelR / R).x"
      :y="point(i, labelR / R).y + labelConfig[i].dy"
      :text-anchor="labelConfig[i].anchor"
      :dominant-baseline="labelConfig[i].baseline"
      font-size="9"
      fill="#7A5C3A"
      font-family="sans-serif"
    >{{ axis.label }}</text>
  </svg>
</template>
