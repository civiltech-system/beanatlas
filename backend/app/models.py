from sqlalchemy import Column, Integer, String, Text, Float
from .database import Base


class Origin(Base):
    __tablename__ = "coffee_origin"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    country_ja = Column(String, nullable=False, default="")
    region = Column(String, nullable=False, default="")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude_min = Column(Integer, default=0)
    altitude_max = Column(Integer, default=0)
    climate = Column(String, default="")
    varieties = Column(Text, default="")       # JSON array stored as text
    process_methods = Column(Text, default="")  # JSON array stored as text
    flavor_notes = Column(Text, default="")    # JSON array stored as text
    acidity = Column(Integer, default=3)
    bitterness = Column(Integer, default=3)
    sweetness = Column(Integer, default=3)
    body = Column(Integer, default=3)
    description = Column(Text, default="")
    description_ja = Column(Text, default="")
    slug = Column(String, unique=True, nullable=False, index=True)
    data_source = Column(String, default="")
