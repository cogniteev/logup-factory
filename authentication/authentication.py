"""
Here stands the authentication mechanism
"""
from datetime import datetime
import time
import bcrypt
from models.models import User, Token
from config import Config


def generate_token(email, password):
    """ Generate a authentication token if given credentials are correct

    @param email: user's email address
    @param password: user's password
    @return: an authentication token upon correct login or None
    """
    user = User.objects(email=email).first()
    if user:
        if str(bcrypt.hashpw(password.encode('utf-8'),
                             user.password.encode('utf-8'))) == user.password:
            return check_user_token(user)
        else:
            return None
    else:
        return None


def refresh_token(token_id, password):
    """ Expands a token validity date upon successful password check

    @param token_id: the token's to refresh id
    @param password: the user's password
    @return: a refreshed token if the password matches or None
    """
    token = Token.find_by_id(token_id)
    user = token.user
    if str(bcrypt.hashpw(password.encode('utf-8'), user.passwd.encode('utf-8')),
           'utf-8') == user.passwd:
        return check_user_token(user)
    else:
        return None


def check_user_token(user):
    """ Retrieve, update or create a user's token

    @param user: the user to get a token for
    @return: a valid token associated with the user
    """
    token = Token.objects(user=user).first()
    valid_limit = datetime.utcfromtimestamp(
        time.time() + Config.TOKEN_VALIDITY
    )

    if token:

        if token.valid_until < valid_limit:
            return token

        else:
            token.valid_until = valid_limit
            token.update()
            return token
    else:
        token = Token(user=user, valid_until=valid_limit)
        token.save()
        return token