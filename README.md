# Account creation bootstrap

Why do we keep doing this boring stuff again and again?

## Requirements

* mongodb
* python
* nodejs
* a [Mailgun](http://www.mailgun.com/) account

## Installation

Copy config file:

```bash
$ cp confs/dev.cfg prod.cfg
```

Compile client code:

```bash
# I assume grunt-cli and bower are installed globally.
# If not, run:
# (sudo) npm install -g grunt-cli bower
$ cd frontend
$ bower install && npm install
$ grunt
```

If you work with _virtualenv_ (you know you should):

```bash
$ virtualenv env
$ source env/bin/activate
```

Then, from the app directory:

```bash
$ pip install -r requirements.txt
$ WEBAPP_SETTINGS=confs/sample.cfg python webapp.py
```

Application will be running on [localhost](http://localhost:5000).
