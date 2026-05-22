import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Origin } from '@/types/origin'
import { fetchOrigins } from '@/api/origins'

export const useOriginsStore = defineStore('origins', () => {
  const origins = ref<Origin[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function loadOrigins() {
    if (origins.value.length > 0) return
    loading.value = true
    error.value = null
    try {
      origins.value = await fetchOrigins()
    } catch (e) {
      error.value = 'Failed to load origins'
    } finally {
      loading.value = false
    }
  }

  return { origins, loading, error, loadOrigins }
})
