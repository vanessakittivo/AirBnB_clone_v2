#!/usr/bin/python3
"""Defines the Place model and its amenity association table."""

import os

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)

from models.base_model import Base, BaseModel


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"),
           primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"),
           primary_key=True, nullable=False),
)


class Place(BaseModel, Base):
    """Represent a rental place."""

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    def __init__(self, *args, **kwargs):
        """Initialize the place and FileStorage amenity ID collection."""
        super().__init__(*args, **kwargs)
        if os.getenv("HBNB_TYPE_STORAGE") != "db" and not hasattr(
                self, "amenity_ids"):
            self.amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        from sqlalchemy.orm import relationship

        user = relationship("User", back_populates="places")
        city = relationship("City", back_populates="places")
        reviews = relationship(
            "Review", back_populates="place", cascade="all, delete-orphan"
        )
        amenities = relationship(
            "Amenity", secondary=place_amenity, viewonly=False
        )
    else:
        @property
        def reviews(self):
            """Return this place's reviews when using FileStorage."""
            from models.review import Review
            from models import storage

            return [review for review in storage.all(Review).values()
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """Return this place's amenities when using FileStorage."""
            from models.amenity import Amenity
            from models import storage

            ids = getattr(self, "amenity_ids", [])
            objects = storage.all(Amenity)
            return [objects[key] for key in objects
                    if objects[key].id in ids]

        @amenities.setter
        def amenities(self, obj):
            """Link an Amenity instance to this place in FileStorage."""
            from models.amenity import Amenity

            if not isinstance(obj, Amenity):
                return
            if not hasattr(self, "amenity_ids"):
                self.amenity_ids = []
            if obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
