from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Float
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


class CoffeeRecord(Base):
    __tablename__ = "coffee_record"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String, nullable=False, index=True)
    origin_id = Column(Integer, ForeignKey("coffee_origin.id"), nullable=True)
    coffee_name = Column(String, nullable=False)
    roaster = Column(String, default="")
    drank_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    brew_method = Column(String, default="")
    roast_level = Column(String, default="")
    rating = Column(Integer, nullable=False, default=3)
    notes = Column(Text, default="")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
