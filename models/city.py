#!/usr/bin/python3
"""Defines the City model."""

import os

from sqlalchemy import Column, ForeignKey, String

from models.base_model import Base, BaseModel


class City(BaseModel, Base):
    """Represent a city belonging to a state."""

    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        from sqlalchemy.orm import relationship

        state = relationship("State", back_populates="cities")
        places = relationship(
            "Place", back_populates="city", cascade="all, delete-orphan"
        )
