#!/usr/bin/python3

""" DB storage """
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
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
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session (self.__session) all objects 
        depending on the class name (argument cls). If cls=None, query all 
        types of objects (User, State, City, Amenity, Place, and Review).
        
        This method returns a dictionary:
        key = <class-name>.<object-id>
        value = object """

        obj_dic = {}

        if cls:
            if cls is str:
                cls = classes.get(cls)
            if cls:
                objects = self.__session.query(cls).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    obj_dic[key] = obj
        else:
            for class_name, class_type in classes.items():
                objects = self.__session.query(class_type).all()
                for obj in objects:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    obj_dic[key] = obj

        return obj_dic

    def new(self, obj):
        """ Adds a new object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Saves all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ creates all the tables in database """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session