export interface Origin {
  id: number
  country: string
  country_ja: string
  region: string
  sub_region?: string     // 県・州・地区レベル（任意）
  farm?: string           // 農園名（任意）
  latitude: number
  longitude: number
  altitude_min: number
  altitude_max: number
  climate: string
  varieties: string[]
  process_methods: string[]
  roast_levels: string[]  // 焙煎度
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
