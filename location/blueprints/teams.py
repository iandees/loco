# -*- coding: utf-8 -*-
from flask import (
    redirect,
    request,
    url_for,
    render_template,
    Blueprint,
)
from flask_login import (
    login_required,
    current_user,
)

from location import models
from location.core import db

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')

@teams_bp.route('/')
@login_required
def index():
    teams = models.Team.query.all()
    return render_template('teams/index.html', teams=teams)

@teams_bp.route('/create', methods=['POST'])
@login_required
def create():
    team = models.Team()
    team.name = request.form['name']
    db.session.add(team)
    db.session.commit()

    return redirect('/teams')

@teams_bp.route('/delete')
@login_required
def delete():
    team = models.Team.query.get(request.args['team_id'])
    db.session.delete(team)
    db.session.commit()

    return redirect('/teams')

@teams_bp.route('/<int:team_id>')
@login_required
def view(team_id):
    team = models.Team.query.get(team_id)
    return render_template('teams/view.html', team=team)


@teams_bp.route('/<int:team_id>/edit', methods=['GET','POST'])
@login_required
def edit(team_id):
    team = models.Team.query.get(team_id)
    all_users = models.User.query.order_by('name')

    if request.method == 'POST':
        checked_user_ids = request.form.getlist('users', int)
        for user in all_users:
            if user.id in checked_user_ids:
                if user not in team.users:
                    team.users.append(user)
            else:
                if user in team.users:
                    team.users.remove(user)

        db.session.add(team)
        db.session.commit()
        return redirect(url_for('teams.edit', team_id=team_id))
    else:
        users_in_team = team.users
        return render_template('teams/edit.html', team=team, all_users=all_users, users_in_team=users_in_team)

@teams_bp.route('/<int:team_id>/join')
@login_required
def join(team_id):
    team = models.Team.query.get(team_id)
    if current_user not in team.users:
        team.users.append(current_user)
        db.session.add(team)
        db.session.commit()
    return redirect('/teams')

@teams_bp.route('/<int:team_id>/leave')
@login_required
def leave(team_id):
    team = models.Team.query.get(team_id)
    if current_user in team.users:
        team.users.remove(current_user)
        db.session.add(team)
        db.session.commit()
    return redirect('/teams')

