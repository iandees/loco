# -*- coding: utf-8 -*-
from flask import (
    redirect,
    url_for,
    render_template,
    request,
    session,
    Blueprint,
    current_app,
)
from flask_oauthlib.client import OAuthException
from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)

from location.core import db, oauth, login_manager
from location import models


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))

    callback = url_for('auth.authorized', _external=True)

    return oauth.google.authorize(callback=callback)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logged_out.html')


@auth_bp.route('/login/authorized')
def authorized():
    resp = oauth.google.authorized_response()

    if resp is None:
        message = "Access denied: reason={} error={}".format(
            request.args['error_reason'],
            request.args['error_description'],
        )
        return render_template('restricted.html', context=dict(message=message)), 400

    if isinstance(resp, OAuthException):
        message = "Access denied: {}".format(
            resp.message
        )
        return render_template('restricted.html', context=dict(message=message)), 400

    session['google_token'] = (resp['access_token'], '')
    info = oauth.google.get('userinfo')

    allowed_domain = current_app.config.get("ALLOWED_DOMAIN")
    if allowed_domain:
        if not info.data['hd'] == allowed_domain:
            message = "Your email is not authorized"
            return render_template('restricted.html', context=dict(message=message)), 400

    user = models.User.query.filter_by(google_id=info.data['id']).first()

    # Save a refreshed access token
    if user and user.google_access_token != resp['access_token']:
        user.google_access_token = resp['access_token']
        db.session.add(user)
        db.session.commit()

    if not user:
        user = models.User(
            google_id=info.data['id'],
            google_access_token=resp['access_token'],
            email=info.data['email'],
            avatar=info.data['picture'],
            name=info.data['name'],
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)

    return redirect(url_for('root.index'))
