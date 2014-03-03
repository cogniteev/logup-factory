"""
Main entry point of the logup-factory
"""

from flask import Flask
from flask.ext.mongoengine import MongoEngine

from flask import request
from flask import session
from flask import jsonify
from flask import render_template

from models.models import User
from authentication.authentication import generate_token

app = Flask(__name__, static_url_path='', static_folder='frontend/dist')
app.config.from_pyfile('flask-conf.cfg')

# db = MongoEngine(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        user = User.create_and_store(request.form['email'],
                                     request.form['password'])
        return jsonify(email=user.email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        token = generate_token(request.form['email'], request.form['password'])
        if token:
            session['token'] = token.id
            return jsonify(email=token.user.email)
        else:
            return jsonify(error='Invalid credentials',
                           fields=['email', 'password'])

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot-password.html')
    else:
        return 'ok'

@app.route('/password-reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if request.method == 'GET':
        return render_template('password-reset.html')
    else:
        return 'ok'

if __name__ == '__main__':
    app.run()
