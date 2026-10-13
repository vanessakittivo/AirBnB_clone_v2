#!/usr/bin/python3
"""Defines the shared BaseModel for AirBnB objects."""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

from models import storage


Base = declarative_base()


class BaseModel:
    """Common fields and behavior shared by persistent model classes."""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize an instance from keyword values or sensible defaults."""
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at") and isinstance(value, str):
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)

        if not getattr(self, "id", None):
            self.id = str(uuid.uuid4())
        if not getattr(self, "created_at", None):
            self.created_at = datetime.utcnow()
        if not getattr(self, "updated_at", None):
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """Return a readable representation of the instance."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    def save(self):
        """Update the modification time and persist the instance."""
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return the instance data in a serialization-friendly dictionary."""
        result = self.__dict__.copy()
        result.pop("_sa_instance_state", None)
        result["__class__"] = self.__class__.__name__
        for key in ("created_at", "updated_at"):
            value = getattr(self, key, None)
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        return result

    def delete(self):
        """Delete this instance from the active storage engine."""
        storage.delete(self)
