import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship

from location.core import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=False)
    google_id = db.Column(db.String(100))
    google_access_token = db.Column(db.Text)

    locations = relationship("Location", lazy="dynamic", order_by="desc(Location.created_at)")

    teams = db.relationship('Team', secondary='team_memberships', backref=db.backref('users', lazy='dynamic'))

    def is_member_of_team(self, team):
        return team in self.teams

    def most_recent_location(self):
        return self.locations.first()

class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

team_memberships = db.Table('team_memberships',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id')),
    db.Column('joined_at', db.DateTime, default=datetime.datetime.utcnow)
)
