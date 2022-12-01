#!/usr/bin/python3
""" Module for defining BaseModel's attributes and methods"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """ defines base model"""

    def __int__(self, *args, **kwargs):
        """ initializing BaseModel

        Args:
            *args (any): argument list
            **kwargs (dict): key/ value pair
        """
        #time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k in ("created_at", "updated_at"):
                    setattr(self, k, datetime.fromisoformat(v))
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.today(self)

    def save(self):
        """
            Update updated_at with the current datetime.
            (Saves Changes made to BaseModel)
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ returns a dictionary for an instance of BaseModel"""
        new_dict = {}
        for k, val in self.__dict__.items():
            if isinstance(val, datetime):
                new_dict[k] = val.isoformat()
            else:
                new_dict[k] = val
        return (new_dict)

    def __str__(self):
        """
        returns str representation of BaseModel
        prints '[<class name>] (<self.id>) <self.__dict__>'
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
