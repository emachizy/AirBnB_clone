#!/usr/bin/python3
""" Filestorage Module"""
import json
from models.base_model import BaseModel


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
        return FileStorage.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id"""
        obj_class = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obj_class, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        obj_st = FileStorage.__objects
        obj_dict = {obj: obj_st[obj].to_dict() for obj in obj_st.keys()}
        with open(FileStoorage.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """deserializes the JSON file to __objects 
        (only if the JSON file (__file_path) exists """
        try:
            with ope(FileStorage.__file_path) as f:
                obj_dict = json.load(f)
                for obj in obj_dict.values()
                cls_name = o["__class__"]
                del obj["__class__"]
                self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
