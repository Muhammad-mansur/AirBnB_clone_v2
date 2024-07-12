#!/usr/bin/python3

""" DB storage """
from sqlalchemy.orm import sessionmaker

class DBStorage:
    """ DB storage class """
    __engine = None
    __session = None
    
    def __init__(self):
        """ create engine """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MSQL_DB')),
                                      pool_pre_ping=True)