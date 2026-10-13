#!/usr/bin/python3
"""Defines the State model."""

import os

from sqlalchemy import Column, String

from models import storage
from models.base_model import Base, BaseModel


class State(BaseModel, Base):
    """Represent a state or region."""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        from sqlalchemy.orm import relationship

        cities = relationship(
            "City", back_populates="state", cascade="all, delete-orphan"
        )
    else:
        @property
        def cities(self):
            """Return this state's cities when using FileStorage."""
            from models.city import City

            return [city for city in storage.all(City).values()
                    if city.state_id == self.id]
