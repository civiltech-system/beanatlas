export interface CoffeeRecordInput {
  origin_id: number | null
  coffee_name: string
  roaster: string
  drank_at: string
  brew_method: string
  roast_level: string
  rating: number
  notes: string
}

export interface CoffeeRecord extends CoffeeRecordInput {
  id: number
  created_at: string
  updated_at: string
}
