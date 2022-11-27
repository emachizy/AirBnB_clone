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
        pass

    def new(self, obj):
        pass

    def save(self):
        pass

    def reload(self):
        pass
