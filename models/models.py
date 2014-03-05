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
    newsletter = BooleanField(required=True)

    @classmethod
    def create_and_store(cls, email, password, newsletter=None):
        """ Create and store a user computing the encrypted password

        @param email: User's email address
        @param password: User's password
        @param newsletter: whether the user subscribe to the newsletter or not
        """
        u = cls(email=email,
                password=bcrypt.hashpw(password.encode('utf-8'),
                                       bcrypt.gensalt()),
                newsletter=newsletter if newsletter else False)
        u.confirmed = False if Config.SIGNUP_REQUIRES_CONFIRMATION else True
        u.save()
        return u


class Token(Document):
    """ The authentication token collection
    """
    user = ReferenceField(User, required=True, unique=True,
                          reverse_delete_rule=CASCADE)


class PasswordRenewToken(Document):
    """ The password token collection
    """
    user = ReferenceField(User, required=True, unique=True,
                          reverse_delete_rule=CASCADE)