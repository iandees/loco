# -*- coding: utf-8 -*-
import os

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth
from flask_login import LoginManager
from flask_caching import Cache
from flask import (
    render_template,
)
env = os.environ.get('LOCO_ENV', 'Local')

db = SQLAlchemy()
migrate = Migrate()
oauth = OAuth()
login_manager = LoginManager()
cache = Cache()


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('restricted.html'), 400
