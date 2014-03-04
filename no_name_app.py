"""
Main entry point of the logup-factory
"""

from flask import Flask
from flask.ext.mongoengine import MongoEngine

from flask import request
from flask import session
from flask import jsonify
from flask import render_template

from models.models import User, Token
from authentication.authentication import generate_token, requires_token, \
    redirect_app
from config import Config
from werkzeug.utils import redirect

app = Flask(__name__, static_url_path='', static_folder='frontend/dist')

def configure_app(config_file_path):
    app.config.from_pyfile(config_file_path)
    app.db = MongoEngine(app)
    return app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app')
@requires_token
def product_home():
    return render_template('user-home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if 'token' in session and is_valid_token(session['token']):
            return redirect('/app')
        else:
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
def forgot_password():
    if request.method == 'GET':
        if 'token' in session and is_valid_token(session['token']):
            return redirect('/app')
        else:
            return render_template('forgot-password.html')
    else:
        return 'ok'

@app.route('/password-reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if request.method == 'GET':
        if 'token' in session and is_valid_token(session['token']):
            return redirect('/app')
        else:
            return render_template('password-reset.html', token=token)
    else:
        return 'ok'

@app.route('/logout', methods=['GET'])
@requires_token
def logout():
    Token.objects(id=session['token']).delete
    session.pop('token', None)
    return jsonify(success=True)

if __name__ == '__main__':
    configure_app('confs/dev-conf.cfg')
    app.run()
