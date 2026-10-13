#!/usr/bin/python3
"""Defines the Review model."""

import os

from sqlalchemy import Column, ForeignKey, String

from models.base_model import Base, BaseModel


class Review(BaseModel, Base):
    """Represent a user's review of a place."""

    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        from sqlalchemy.orm import relationship

        place = relationship("Place", back_populates="reviews")
        user = relationship("User", back_populates="reviews")
