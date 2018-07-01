# -*- coding: utf-8 -*-
from flask import Flask, session
from flask_sslify import SSLify
from werkzeug.contrib.fixers import ProxyFix

from location.core import env, db, migrate, oauth, login_manager, cache
from location import blueprints


def create_app(package_name):
    app = Flask(package_name, instance_relative_config=True)

    config_name = "location.config.{}".format(env)
    app.config.from_object(config_name)

    cache.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    sslify = SSLify(app)

    oauth.init_app(app)
    google = oauth.remote_app(
        'google',
        consumer_key=app.config.get('GOOGLE_CLIENT_ID'),
        consumer_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        request_token_params={
            'scope': 'email profile',
            'hd': app.config.get('ALLOWED_DOMAIN'),
        },
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
    )

    @google.tokengetter
    def get_access_token():
        return session.get('google_token')

    login_manager.init_app(app)

    app.register_blueprint(blueprints.root_bp)
    app.register_blueprint(blueprints.auth_bp)
    app.register_blueprint(blueprints.locations_bp)
    app.register_blueprint(blueprints.teams_bp)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
