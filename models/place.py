#!/usr/bin/python3
"""Place Module."""
from models.base_model import BaseModel


class Place(BaseModel):
    """ Defines place

        Attributes:
           city_id (string): it will be the City.id
           user_id (string): it will be the User.id
           name (str): name of place
           description (str): description of place
           number_rooms (int): number of rooms
           number_bathrooms (int): number of bathrooms
           max_guest (int): max number of guests
           price_by_night(int): cost for a night
           latitude (float): latidinal location
           longitude (float): longitudinal location
           amenity_ids (list): list of Amenity ID
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms =  0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
