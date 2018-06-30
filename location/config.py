import os

class Base(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    ALLOWED_DOMAIN = os.environ.get('ALLOWED_DOMAIN')

    ON_HEROKU = os.environ.get('ON_HEROKU')

    SECRET_KEY = 'development key'
    DEBUG = True

class Heroku(Base):
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL')

class Production(Heroku):
    pass

class Local(Base):
    CACHE_TYPE = 'simple'
