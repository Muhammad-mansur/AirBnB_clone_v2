#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state")
        
    @property
    def cities(self):
        """ Getter attribute cities that returns list of City instances"""
        from models import storage
        cities_list = []
        cities_dict = storage.all("City")
        for city_id, city_obj in cities_dict.items():
            if city_obj.state_id == self.id:
                cities_list.append(city_obj)
        return cities_list