import json
from datetime import datetime
from pydantic import BaseModel, field_validator


class OriginResponse(BaseModel):
    id: int
    country: str
    country_ja: str
    region: str
    latitude: float
    longitude: float
    altitude_min: int
    altitude_max: int
    climate: str
    varieties: list[str]
    process_methods: list[str]
    flavor_notes: list[str]
    acidity: int
    bitterness: int
    sweetness: int
    body: int
    description: str
    description_ja: str
    slug: str
    data_source: str

    @field_validator("varieties", "process_methods", "flavor_notes", mode="before")
    @classmethod
    def parse_json_list(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                return []
        return v or []

    model_config = {"from_attributes": True}


class CoffeeRecordInput(BaseModel):
    origin_id: int | None = None
    coffee_name: str
    roaster: str = ""
    drank_at: datetime
    brew_method: str = ""
    roast_level: str = ""
    rating: int = 3
    notes: str = ""

    @field_validator("coffee_name")
    @classmethod
    def validate_coffee_name(cls, value: str):
        value = value.strip()
        if not value:
            raise ValueError("coffee_name is required")
        if len(value) > 200:
            raise ValueError("coffee_name is too long")
        return value

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, value: int):
        if not 1 <= value <= 5:
            raise ValueError("rating must be between 1 and 5")
        return value


class CoffeeRecordResponse(CoffeeRecordInput):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
