#!/usr/bin/python3

""" DB storage """
from sqlalchemy.orm import sessionmaker

class DBStorage:
    """ DB storage class """
    __engine = None
    __session = None
    
    def __init__(self):
        """ create engine """