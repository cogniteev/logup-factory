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
  email = EmailField()
  password = StringField()
  confirmed = BooleanField()

  @classmethod
  def create_and_store(cls, email, password):
    """ Create and store a user computing the encrypted password

    @param email: User's email address
    @param password: User's password
    """
    u = cls(email=email, passwd=bcrypt.hashpw(password.encode('utf-8'),
                                              bcrypt.gensalt()))
    u.confirmed = False if Config.SIGNUP_REQUIRES_CONFIRMATION else True
    u.save()