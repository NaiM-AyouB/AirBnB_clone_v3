#!/usr/bin/python3
""" holds class User"""
import models
import hashlib
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            if "hashed_password" in kwargs:
                self._password = kwargs.pop('hashed_password')
            if "password" in kwargs:
                self.password = kwargs.pop('password')
        super().__init__(*args, **kwargs)

    def to_md5(self, raw_password):
        """I'm the 'password' property."""
        secure = hashlib.md5()
        secure.update(raw_password.encode("utf-8"))
        return secure.hexdigest()

    @property
    def password(self):
        """I'm the 'password' property."""
        return self._password

    @password.setter
    def password(self, raw_password):
        """I'm the 'password' property."""
        self._password = self.to_md5(raw_password)
