#!/usr/bin/python3
"""Reviews Module."""
from models.base_model import BaseModel


class Review(BaseModel):
    """ Defines review

        Attributes:
            place_id (str): ID of location
            user_id (str): ID of user that gave review
            text (str): review text
    """

    place_id = ""
    user_id = ""
    text = ""
