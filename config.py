import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(basedir, 'appointment.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
SECRET_KEY = 'SECRET_LANG'
JWT_AUTH_URL_RULE = '/login'
JWT_AUTH_USERNAME_KEY = 'email'

PORT = 5000
HOST = '127.0.0.1'
