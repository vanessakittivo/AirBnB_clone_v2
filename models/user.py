#!/usr/bin/python3
"""Defines the User model."""

import os

from sqlalchemy import Column, String

from models.base_model import Base, BaseModel


class User(BaseModel, Base):
    """Represent an application user."""

    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        from sqlalchemy.orm import relationship

        places = relationship(
            "Place", back_populates="user", cascade="all, delete-orphan"
        )
        reviews = relationship(
            "Review", back_populates="user", cascade="all, delete-orphan"
        )
