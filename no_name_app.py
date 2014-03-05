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
from werkzeug.utils import redirect

app = Flask(__name__, static_url_path='', static_folder='frontend/dist')


def configure_app(config_file_path):
    app.config.from_pyfile(config_file_path)
    app.db = MongoEngine(app)
    app.mailgun_client = Client(app.config['MAILGUN_API_KEY'],
                                app.config['MAILGUN_DOMAIN'])
    return app


@app.before_request
def before_request():
    if 'token' in session:
        t = Token.objects(id=session['token'])
        u = t.first()
        if u:
            g.current_user = {'email': u.user.email}
        else:
            g.current_user = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/app')
@requires_token
def product_home():
    return render_template('user-home.html')


@app.route('/signup', methods=['GET', 'POST'])
@redirect_app
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        if User.objects(email=request.form['email']).count() > 0:
            return jsonify(error='Already registered email')

        elif not Config.EMAIL_REGEX.match(request.form['email']):
            return jsonify(error='Invalid email address')

        else:
            user = User.create_and_store(
                request.form['email'],
                request.form['password']
            )
            return jsonify(email=user.email)


@app.route('/login', methods=['GET', 'POST'])
@redirect_app
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        token = generate_token(request.form['email'], request.form['password'])
        if token:
            session['token'] = str(token.id)
            return jsonify(email=token.user.email)
        else:
            return jsonify(error='Invalid credentials')


@app.route('/forgot-password', methods=['GET', 'POST'])
@redirect_app
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot-password.html')
    else:
        users = User.objects(email=request.form['email'])
        if users.count() > 0:
            user = users.first()
            if PasswordRenewToken.objects(user=user).count() > 0:
                renew_token = PasswordRenewToken.objects(user=user).first()
                hashed = b64encode(str(renew_token.id))
            else:
                renew_token = PasswordRenewToken(user=user)
                renew_token.save()
                hashed = b64encode(str(renew_token.id))
            reset_link = url_for('password_reset', token=hashed, _external=True)
            answer = send_password_reset(app.mailgun_client,
                                         app.config['MAILGUN_MAILING_ADDRESS'],
                                         user.email,
                                         reset_link)
            if answer.status_code == 200:
                return jsonify(success=True)
            else:
                return jsonify(error='Unable to sent mail')
        else:
            return jsonify(error='Unknown email')


@app.route('/password-reset/<token>', methods=['GET', 'POST'])
@redirect_app
def password_reset(token):
    if request.method == 'GET':
        return render_template('password-reset.html', token=token)
    else:
        try:
            clear = b64decode(token)
        except TypeError:
            return jsonify(error='Invalid reset request')

        p_token = PasswordRenewToken.objects(id=clear)
        if p_token.count() > 0:
            p_token.first().user.update_password(request.form['password'])
            p_token.delete()
            return jsonify(success=True)
        else:
            return jsonify(error='Invalid reset request')


@app.route('/logout', methods=['GET'])
@requires_token
def logout():
    Token.objects(id=session['token']).delete
    session.pop('token', None)
    return jsonify(success=True)


@app.route('/request-beta-access', methods=['POST'])
def request_beta_access():
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
