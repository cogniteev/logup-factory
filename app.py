"""
Main entry point of the logup-factory
"""

from flask import Flask
from flask.ext.mongoengine import MongoEngine

from flask import request
from flask import render_template

app = Flask(__name__)
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
        return 'ok'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        return 'ok'

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
