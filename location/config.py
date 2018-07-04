import os

from location.oauth_providers import GOOGLE


class Base(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    ALLOWED_DOMAIN = os.environ.get('ALLOWED_DOMAIN')
    DEFAULT_AVATAR = os.environ.get('DEFAULT_AVATAR', 'static/images/avatars/default.png')

    OAUTH_PROVIDER = os.environ.get('OAUTH_PROVIDER', GOOGLE)
    OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID')
    OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET')

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
