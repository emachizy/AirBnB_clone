#!/usr/bin/python3
""" Filestorage Module"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """ storage engine
        Attributes:
        __file_path (str): JSON path
        __objects (dict): dictionay of objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id"""
        obj_class = obj.__class__.__name__
        self.__objects["{}.{}".format(obj_class, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        
        with open(self.__file_path, mode='w') as file:
            json_objs = {}
            for key, value in self.__objects.items():
                json_objs[key] = value.to_dict()
            file.write(json.JSONEncoder().encode(json_objs))

    def reload(self):
        """
            deserializes the JSON file to __objects
            (only if the JSON file (__file_path) exists
        """
        try:
            if os.path.isfile(self.__file_path):
                file_lines = []
                with open(self.__file_path, mode='r') as file:
                    file_lines = file.readlines()
                file_txt = ''.join(file_lines) if len(file_lines) > 0 else '{}'
                json_objs = json.JSONDecoder().decode(file_txt)
                base_model_objs = dict()
                classes = self.model_classes
                for key, value in json_objs.items():
                    cls_name = value['__class__']
                    if cls_name in classes.keys():
                        base_model_objs[key] = classes[cls_name](**value)
                self.__objects = base_model_objs
        except FileNotFoundError:
            return
