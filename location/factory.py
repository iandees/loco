# -*- coding: utf-8 -*-
from flask import Flask, session
from flask_sslify import SSLify
from werkzeug.contrib.fixers import ProxyFix

from location import blueprints, oauth_providers
from location.core import cache, db, env, login_manager, migrate, oauth


def create_app(package_name):
    app = Flask(package_name, instance_relative_config=True)

    config_name = "location.config.{}".format(env)
    app.config.from_object(config_name)

    cache.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    sslify = SSLify(app)

    oauth.init_app(app)
    app.oauth_provider = oauth_providers.get_provider(
        app.config.get('OAUTH_PROVIDER'),
        app.config.get('OAUTH_CLIENT_ID'),
        app.config.get('OAUTH_CLIENT_SECRET'),
        app.config.get('ALLOWED_DOMAIN')
    )
    oauth_app = oauth.remote_app(**app.oauth_provider.settings())

    @oauth_app.tokengetter
    def get_access_token():
        return session.get('access_token')

    login_manager.init_app(app)

    app.register_blueprint(blueprints.root_bp)
    app.register_blueprint(blueprints.auth_bp)
    app.register_blueprint(blueprints.locations_bp)
    app.register_blueprint(blueprints.teams_bp)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
