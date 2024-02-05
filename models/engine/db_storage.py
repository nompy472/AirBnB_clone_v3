#!/usr/bin/python3
"""Contains the class DBStorage"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Fetches all the objects of a particular class in a
        session or all the classes
        """

        objs = {}
        if cls:
            if type(cls) == str:
                cls = globals()[cls]

            for obj in self.__session.query(cls).all():
                key = cls.__name__ + '.' + obj.id
                objs[key] = obj

        else:
            for table in Base.metadata.tables.values():
                for obj in self.__session.query(table):
                    key = table.__name__ + '.' + obj.id
                    objs[key] = obj

        return objs

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def delete_relationship(self, parent, child):
        """Removes a many-many relationship between two objects"""
        parent.delete_relationship(child.id)
        self.__session.add(parent)
        self.__session.commit()

    def create_relationship(self, parent, child):
        """Creates a many-many relationship between two objects"""
        parent.create_relationship(child.id)
        self.__session.add(parent)
        self.__session.commit()

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Calls remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID,
        Else None
        """
        return self.__session.query(cls).get(id)

        # if cls not in classes.values():
        #     return None

        # all_cls = models.storage.all(cls)
        # for value in all_cls.values():
        #     if (value.id == id):
        #         return value

        # return None

    def count(self, cls=None):
        """Counts number of objects in storage
        """
        return len(self.all(cls))
        # all_class = classes.values()

        # if not cls:
        #     count = 0
        #     for clas in all_class:
        #         count += len(models.storage.all(clas).values())
        # else:
        #     count = len(models.storage.all(cls).values())

        # return count
