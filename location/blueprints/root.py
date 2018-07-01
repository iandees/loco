# -*- coding: utf-8 -*-
from flask import (
    redirect,
    url_for,
    render_template,
    Blueprint,
)
from flask_login import (
    current_user,
)

root_bp = Blueprint('root', __name__)


@root_bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return redirect(url_for('auth.login'))
