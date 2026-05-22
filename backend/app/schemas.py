import json
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
