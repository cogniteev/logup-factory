"""
This module contains the user's mongo description
"""

from mongoengine import *
from config import Config

import bcrypt


class User(Document):
    """
    The application user collection
    """
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    confirmed = BooleanField(required=True)

    @classmethod
    def create_and_store(cls, email, password):
        """ Create and store a user computing the encrypted password

        @param email: User's email address
        @param password: User's password
        """
        u = cls(email=email, password=bcrypt.hashpw(password.encode('utf-8'),
                                                  bcrypt.gensalt()))
        u.confirmed = False if Config.SIGNUP_REQUIRES_CONFIRMATION else True
        u.save()
        return u


class Token(Document):
    """ The authentication token collection
    """
    user = ReferenceField(User, required=True, unique=True,
                          reverse_delete_rule=CASCADE)