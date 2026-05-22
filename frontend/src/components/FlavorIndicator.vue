<script setup lang="ts">
defineProps<{ label: string; value: number }>()
</script>

<template>
  <div class="flex items-center gap-3">
    <span class="text-sm text-coffee-500 w-24">{{ label }}</span>
    <div class="flex gap-1">
      <span
        v-for="i in 5"
        :key="i"
        class="w-2 h-2 rounded-full transition-colors"
        :class="i <= value ? 'bg-coffee-500' : 'bg-coffee-100'"
      />
    </div>
  </div>
</template>
