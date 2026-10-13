#!/usr/bin/python3
"""SQLAlchemy-backed storage engine for the AirBnB project."""

import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """Persist model instances in a MySQL database through SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self):
        """Create the MySQL engine using the configured environment values."""
        username = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        database = os.getenv("HBNB_MYSQL_DB")
        missing = [
            name for name, value in (
                ("HBNB_MYSQL_USER", username),
                ("HBNB_MYSQL_PWD", password),
                ("HBNB_MYSQL_DB", database),
            ) if value is None
        ]
        if missing:
            raise RuntimeError(
                "Set the MySQL environment variables: {}".format(
                    ", ".join(missing)
                )
            )

        url = "mysql+mysqldb://{}:{}@{}/{}".format(
            quote_plus(username),
            quote_plus(password),
            host,
            database,
        )
        self.__engine = create_engine(url, pool_pre_ping=True)

    def all(self, cls=None):
        """Return stored objects, optionally restricted to one model class."""
        models = self._model_classes()
        classes = (cls,) if cls is not None else models
        objects = {}
        for model in classes:
            for obj in self.__session.query(model).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        return objects

    def new(self, obj):
        """Add an object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session if provided."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Load mapped models, create tables, and start a thread-safe session."""
        from models.base_model import Base
        self._model_classes()

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(factory)

    def close(self):
        """Remove the current thread's session from the scoped registry."""
        if self.__session is not None:
            self.__session.remove()

    @staticmethod
    def _model_classes():
        """Import and return all persistent classes before metadata operations."""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        return (User, State, City, Amenity, Place, Review)
