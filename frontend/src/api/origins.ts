import type { Origin } from '@/types/origin'

const BASE = '/api/v1'

export async function fetchOrigins(): Promise<Origin[]> {
  const res = await fetch(`${BASE}/origins`)
  if (!res.ok) throw new Error('Failed to fetch origins')
  return res.json()
}

export async function fetchOrigin(slug: string): Promise<Origin> {
  const res = await fetch(`${BASE}/origins/${slug}`)
  if (!res.ok) throw new Error('Failed to fetch origin')
  return res.json()
}
