#!/usr/bin/python3
"""Defines the FileStorage class."""

import json


class FileStorage:
    """Serializes and deserializes objects to and from a JSON file."""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return all objects, optionally filtered by class."""
        if cls is None:
            return self.__objects

        return {
            key: obj
            for key, obj in self.__objects.items()
            if isinstance(obj, cls)
        }

    def new(self, obj):
        """Add an object to the storage dictionary."""
        key = "{}.{}".format(
            obj.__class__.__name__,
            obj.id
        )
        self.__objects[key] = obj

    def delete(self, obj=None):
        """Delete an object from storage if it exists."""
        if obj is None:
            return

        key = "{}.{}".format(
            obj.__class__.__name__,
            obj.id
        )

        if key in self.__objects:
            del self.__objects[key]

    def save(self):
        """Serialize objects and save them to the JSON file."""
        objects_dict = {}

        for key, obj in self.__objects.items():
            objects_dict[key] = obj.to_dict()

        with open(self.__file_path, "w") as file:
            json.dump(objects_dict, file)

    def reload(self):
        """Deserialize the JSON file to objects."""
        try:
            with open(self.__file_path, "r") as file:
                objects_dict = json.load(file)
        except FileNotFoundError:
            return

        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review
        }

        for key, value in objects_dict.items():
            class_name = value["__class__"]
            self.__objects[key] = classes[class_name](**value)
