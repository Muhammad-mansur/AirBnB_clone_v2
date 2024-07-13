#!/usr/bin/python3

""" DB storage """
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models. place import Place
from models.review import Review

classes = {
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review
        }

class DBStorage:
    """ DB storage class """
    __engine = None
    __session = None
    
    def __init__(self):
        """ create engine """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(user, pwd, host, db)
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ All """
        obj_dic = {}

        if cls:
            if cls is str:
                cls = classes.get(cls)
            if cls:
                objects = self.__session.query(cls).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    obj_dic[key] = obj