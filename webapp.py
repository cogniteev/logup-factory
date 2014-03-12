"""
Main entry point of the logup-factory
"""
from base64 import b64encode, b64decode

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask import request
from flask import session
from flask import jsonify
from flask import render_template
from flask import url_for
from flask import g
from models.models import User, Token, PasswordRenewToken, BetaRequest
from authentication.authentication import generate_token
from authentication.authentication import requires_token
from authentication.authentication import redirect_app
from utils.mailgun_helper import send_password_reset
from python_mailgun.client import Client
from config import Config
from werkzeug.exceptions import abort

app = Flask(__name__, static_url_path='', static_folder='frontend/dist')


def configure_app(config_file_path):
    """ Function to be called for flask's configuration

    @param config_file_path: the configuration's file path
    @return: the configured app
    """
    app.config.from_pyfile(config_file_path)
    app.db = MongoEngine(app)
    app.mailgun_client = None
    if 'MAILGUN_API_KEY' and 'MAILGUN_DOMAIN' in app.config:
        app.mailgun_client = Client(app.config['MAILGUN_API_KEY'],
                                    app.config['MAILGUN_DOMAIN'])
    return app


@app.before_request
def get_user_info():
    """ function to executed before each received request

    Will test if the user is authenticated and consequently insert its
    information into the g variable
    """
    if 'token' in session:
        t = Token.objects(id=session['token'])
        u = t.first()
        if u:
            g.current_user = {'email': u.user.email}
        else:
            g.current_user = None


@app.route('/')
def index():
    """ Application's index

    @return: rendering for the index page
    """
    return render_template('index.html')


@app.route('/app')
@requires_token
def product_home():
    """ Product's home

    @return: rendering for the product's home page or a 401 (Unauthorized)
    response caused by the requires_token wrapper
    """
    return render_template('user-home.html')


@app.route('/signup', methods=['GET'])
@redirect_app
def signup_page():
    """ Signup page

    @return: rendering for the signup page
    """
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup():
    """ Signup endpoint

    Attempt to register a user to the website
    @return: A json response containing an email field upon success or an
    error description
    """
    if not Config.EMAIL_REGEX.match(request.form['email']):
        return jsonify(error='Invalid email address')

    elif User.objects(email=request.form['email']).count() > 0:
        return jsonify(error='Already registered email')

    else:
        user = User.create_and_store(
            request.form['email'],
            request.form['password']
        )
        return jsonify(email=user.email)


@app.route('/login', methods=['GET'])
@redirect_app
def login_page():
    """ Login page

    @return: rendering for the login page
    """
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    """ login endpoint

    Attempt to login a user
    @return: A json response containing an email field upon success or an
    error description
    """
    token = generate_token(request.form['email'], request.form['password'])
    if token:
        session['token'] = str(token.id)
        return jsonify(email=token.user.email)
    else:
        return jsonify(error='Invalid credentials')


@app.route('/forgot-password', methods=['GET'])
@redirect_app
def forgot_password_page():
    """ The forgot password page

    Render the forgot password page if a mailgun configuration is provided
    @return: rendering for the forgot password page if a mailgun client is
    configured or abort with 404 (not found) status code
    """
    if app.mailgun_client:
        return render_template('forgot-password.html')
    else:
        return abort(404)


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    """ The forgot password endpoint

    Attempt to create an url to be sent for password reset
    @return: The json answer {'success': true} upon successful email generation
    and sending  or an error description. If no mailgun configuration is
    provided abort with 404 (not found) status code
    """
    if not app.mailgun_client:
        abort(404)

    users = User.objects(email=request.form['email'])
    if users.count() == 0:
        return jsonify(error='Unknown email')
    user = users.first()
    if PasswordRenewToken.objects(user=user).count() > 0:
        renew_token = PasswordRenewToken.objects(user=user).first()
        hashed = b64encode(str(renew_token.id))
    else:
        renew_token = PasswordRenewToken(user=user)
        renew_token.save()
        hashed = b64encode(str(renew_token.id))
    reset_link = url_for('password_reset', token=hashed, _external=True)

    answer = send_password_reset(
        app.mailgun_client,
        app.config['MAILGUN_MAILING_ADDRESS'],
        user.email,
        render_template('email/forgot-password.txt', link=reset_link),
        render_template('email/forgot-password.html', link=reset_link)
    )

    if answer.status_code == 200:
        return jsonify(success=True)
    else:
        return jsonify(error='Unable to sent mail')



@app.route('/password-reset/<token>', methods=['GET'])
@redirect_app
def password_reset_page(token):
    """ Password reset page

    @param token: the token url parameter
    @return: rendering for the password reset page
    """
    return render_template('password-reset.html', token=token)


@app.route('/password-reset/<token>', methods=['POST'])
@redirect_app
def password_reset(token):
    """ Password reset endpoint

    @param token: the token url parameter
    @return: The json answer {'success': true} upon successful reset or an error
    description
    """
    try:
        clear = b64decode(token)
    except TypeError:
        return jsonify(error='Invalid reset request')

    p_token = PasswordRenewToken.objects(id=clear)
    if p_token.count() == 0:
        return jsonify(error='Invalid reset request')
    p_token.first().user.update_password(request.form['password'])
    p_token.delete()
    return jsonify(success=True)


@app.route('/logout', methods=['GET'])
@requires_token
def logout():
    """ The logout endpoint

    Attempt to logout the user and delete its token from mongoDB
    @return: {'success': true} upon successful logout or a 401 (Unauthorized)
    response caused by the requires_token wrapper
    """
    Token.objects(id=session['token']).delete()
    session.pop('token', None)
    return jsonify(success=True)


@app.route('/request-beta-access', methods=['POST'])
def request_beta_access():
    """ request beta access endpoint

    Attempt to add the user to the beta request list
    @return: {'success': true} upon successful subscription or an error
    description
    """
    email = request.form['email']
    if not Config.EMAIL_REGEX.match(email):
        return jsonify(error='Invalid email address')

    if User.objects(email=email).count() == 0 and BetaRequest.objects(
            email=email).count() == 0:
        BetaRequest(email=email, code=request.form['promo_code']).save()
        return jsonify(success=True)
    else:
        return jsonify(error='Already registered')


if __name__ == '__main__':
    configure_app('confs/prod.cfg')
    app.run(threaded=True)
