#!/usr/bin/python3
"""Command interpreter for the AirBnB project."""

import cmd
import shlex

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """Simple command interpreter for AirBnB objects."""

    prompt = "(hbnb) "

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_create(self, arg):
        """Create a new instance of a class and print its id."""
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        obj = self.classes[class_name]()

        for param in args[1:]:
            if "=" not in param:
                continue

            key, value = param.split("=", 1)

            if not key or not value:
                continue

            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
                value = value.replace("_", " ")
                value = value.replace('\\"', '"')
            else:
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass

            setattr(obj, key, value)

        obj.save()
        print(obj.id)

    def do_show(self, arg):
        """Print the string representation of an instance."""
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        print(objects[key])

    def do_destroy(self, arg):
        """Delete an instance based on class name and id."""
        args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        del objects[key]
        storage.save()

    def do_all(self, arg):
        """Print all instances, optionally filtered by class."""
        args = arg.split()
        objects = storage.all()

        if len(args) > 0:
            class_name = args[0]

            if class_name not in self.classes:
                print("** class doesn't exist **")
                return

            result = [
                str(obj)
                for obj in objects.values()
                if obj.__class__.__name__ == class_name
            ]
        else:
            result = [str(obj) for obj in objects.values()]

        print(result)

    def do_update(self, arg):
        """Update one attribute of an existing instance."""
        args = shlex.split(arg)

        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]

        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        attr_name = args[2]
        value = args[3]
        obj = objects[key]

        if hasattr(obj, attr_name):
            current_value = getattr(obj, attr_name)

            if isinstance(current_value, int):
                value = int(value)
            elif isinstance(current_value, float):
                value = float(value)

        setattr(obj, attr_name, value)
        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
