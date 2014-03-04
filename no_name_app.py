"""
Main entry point of the logup-factory
"""

from flask import Flask
from flask.ext.mongoengine import MongoEngine

from flask import request
from flask import session
from flask import jsonify
from flask import make_response
from flask import render_template

from models.models import User, Token
from authentication.authentication import generate_token, requires_token
from config import Config

app = Flask(__name__, static_url_path='', static_folder='frontend/dist')
app.config.from_pyfile('flask-conf.cfg')

db = MongoEngine(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        if User.objects(email=request.form['email']).count() > 0:
            return make_response(jsonify(error='Already registered email'), 412)

        elif not Config.EMAIL_REGEX.match(request.form['email']):
            return make_response(jsonify(error='Invalid email address'), 412)

        else:
            user = User.create_and_store(
                request.form['email'],
                request.form['password']
            )
            return jsonify(email=user.email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        token = generate_token(request.form['email'], request.form['password'])
        if token:
            session['token'] = str(token.id)
            return jsonify(email=token.user.email)
        else:
            return make_response(jsonify(error='Invalid credentials'), 401)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot-password.html')
    else:
        return 'ok'

@app.route('/password-reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if request.method == 'GET':
        return render_template('password-reset.html', token=token)
    else:
        return 'ok'

@app.route('/logout', methods=['GET'])
@requires_token
def logout():
    Token.objects(id=session['token']).delete
    session.pop('token', None)
    return make_response(jsonify(success=True), 200)

if __name__ == '__main__':
    app.run()
