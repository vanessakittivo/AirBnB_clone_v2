#!/usr/bin/python3
"""Defines the Amenity model."""

import os

from sqlalchemy import Column, String

from models.base_model import Base, BaseModel


class Amenity(BaseModel, Base):
    """Represent an amenity that can be linked to multiple places."""

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        from sqlalchemy.orm import relationship

        place_amenities = relationship(
            "Place", secondary="place_amenity", viewonly=False
        )
