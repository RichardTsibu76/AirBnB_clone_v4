#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import FILE_PATH

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = FILE_PATH

    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls in [value.__class__, value.__class__.__name__]:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key, value in self.__objects.items():
            json_objects[key] = value.to_dict()

        with open(self.__file_path, 'w', encoding="utf-8") as f:
            json.dump(json_objects, f, indent=4)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r', encoding="utf-8") as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except IOError:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it's inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def count(self, cls=None):
        """
        Returns the number of objects in the storage.

        Args:
            cls (optional): The class name of the objects to count.
            If not provided, counts all objects.

        Returns:
            int: The number of objects in the storage.
        """
        return len(self.all(cls))

    def get(self, cls=None, cls_id=None):
        """
        Retrieve an object from the storage based on the class and ID.

        Args:
            cls (type): The class of the object to retrieve.
            cls_id (str): The ID of the object to retrieve.

        Returns:
            object: The retrieved object, or None if not found.
        """
        if None in [cls, cls_id]:
            return None

        key = "{}.{}".format(cls.__name__, cls_id)
        return self.__objects.get(key)
