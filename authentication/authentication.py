"""
Here stands the authentication mechanism
"""
from functools import wraps

import bcrypt
from flask import session, request
from models.models import User, Token
from werkzeug.exceptions import abort
from werkzeug.utils import redirect


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


def check_user_token(user):
    """ Retrieve, update or create a user's token

    @param user: the user to get a token for
    @return: a valid token associated with the user
    """
    token = Token.objects(user=user).first()

    if token:
        return token
    else:
        token = Token(user=user)
        token.save()
        return token


def is_valid_token(token_id):
    """ Check the existence of a token into mongoDB

    @param token_id: the token's to test id
    @return: whether the token is valid (exists) or not
    """
    return Token.objects(id=token_id).count() > 0


def redirect_app(f):
    """ Wrapper allowing to redirect an authenticated user to the app page

    @param f: the function to wrap
    @return: a redirection if authenticated or the given function result
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """ The wraps decorator

        @param args: initial f's args
        @param kwargs: initial f's kwargs
        @return: a redirection if authenticated or f
        """
        if request.method == 'GET' and 'token' in session and is_valid_token(
                session['token']):
            return redirect('/app')
        else:
            return f(*args, **kwargs)

    return decorated


def requires_token(f):
    """ Wrapper allowing to filter calls only for token authenticated users

    @param f: the function to wrap
    @return: a unauthorized answer or the given function result
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        """ The wraps decorator

        @param args: initial f's args
        @param kwargs: initial f's kwargs
        @return: an abortion if unauthorized or f
        """
        if 'token' in session:
            t = Token.objects(id=session['token'])
            return f(*args, **kwargs) if t.count > 0 else abort(401)
        else:
            return abort(401)

    return decorated
