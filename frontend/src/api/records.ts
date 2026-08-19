import { useAuthStore } from '@/stores/auth'
import type { CoffeeRecord, CoffeeRecordInput } from '@/types/record'

const BASE = '/api/v1/records'

async function authenticatedFetch(path = '', init: RequestInit = {}) {
  const token = await useAuthStore().getIdToken()
  const response = await fetch(`${BASE}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...init.headers,
    },
  })
  if (!response.ok) {
    const body = await response.json().catch(() => null)
    throw new Error(body?.detail ?? '記録の処理に失敗しました')
  }
  return response
}

export async function fetchRecords(): Promise<CoffeeRecord[]> {
  return (await authenticatedFetch()).json()
}

export async function createRecord(input: CoffeeRecordInput): Promise<CoffeeRecord> {
  return (await authenticatedFetch('', { method: 'POST', body: JSON.stringify(input) })).json()
}

export async function updateRecord(id: number, input: CoffeeRecordInput): Promise<CoffeeRecord> {
  return (await authenticatedFetch(`/${id}`, { method: 'PUT', body: JSON.stringify(input) })).json()
}

export async function deleteRecord(id: number): Promise<void> {
  await authenticatedFetch(`/${id}`, { method: 'DELETE' })
}
