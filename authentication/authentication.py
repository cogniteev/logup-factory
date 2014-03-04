"""
Here stands the authentication mechanism
"""
from datetime import datetime
from functools import wraps
import time
import bcrypt
from flask import session
from models.models import User, Token
from config import Config
from werkzeug.exceptions import abort


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
    extended = datetime.utcfromtimestamp(
        time.time() + Config.TOKEN_VALIDITY
    )
    now = datetime.utcfromtimestamp(time.time())

    if token:
        return token
    else:
        token = Token(user=user)
        token.save()
        return token

def requires_token(f):


    @wraps(f)
    def decorated(*args, **kwargs):

        if 'token' in session:
            t = Token.objects(id=session['token'])
            return f(*args, **kwargs) if t.count > 0 else abort(401)
        else:
            return abort(401)

    return decorated