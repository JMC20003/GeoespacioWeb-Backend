# app/models/feature_model.py
from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry(geometry_type="GEOMETRY", srid=4326))  # cualquier geometría
    properties = Column(JSONB)
