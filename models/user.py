#!/usr/bin/python3
"""User Module"""
from models.base_model import BaseModel


class User(BaseModel):
    """ Defines User 

        Attributes:
            email (str): user email
            password (str): usr password
            first_name (str): user first name
            last_name (str): user last name
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
