export interface Origin {
  id: number
  country: string
  country_ja: string
  region: string
  latitude: number
  longitude: number
  altitude_min: number
  altitude_max: number
  climate: string
  varieties: string[]
  process_methods: string[]
  flavor_notes: string[]
  acidity: number
  bitterness: number
  sweetness: number
  body: number
  description: string
  description_ja: string
  slug: string
  data_source: string
}
