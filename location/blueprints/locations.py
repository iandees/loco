# -*- coding: utf-8 -*-
from flask import (
    current_app,
    jsonify,
    request,
    Blueprint,
)
from flask_login import (
    login_required,
    current_user,
)

from location.core import db, cache
from location import models

locations_bp = Blueprint('locations', __name__)


@locations_bp.route('/locations/me', methods=['POST'])
@login_required
def save():
    location = models.Location(
        user_id=current_user.id,
        lat=request.json['lat'],
        lon=request.json['lon'],
        description=request.json['description'],
    )
    db.session.add(location)
    db.session.commit()

    # Clear the get_locations cache when someone updates their location
    cache.delete_memoized(get_locations)

    return jsonify({"location": "added"})


@locations_bp.route('/locations.geojson', methods=['GET'])
# TODO: reenable caching.
# @cache.cached()
@login_required
def get_locations():
    data = []

    team_id = request.args.get('team_id')
    if team_id is not None:
        team = models.Team.query.get(int(team_id))
        users = team.users.all()
    else:
        users = models.User.query.all()

    for user in users:
        loc = user.most_recent_location()
        if loc:
            data.append({
                "type": "Feature",
                "properties": {
                    "name": user.name,
                    "description": loc.description,
                    "id": user.id,
                    "avatar": user.avatar or current_app.config.get('DEFAULT_AVATAR'),
                    "last_updated": loc.created_at.isoformat() + '+00:00',
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        loc.lon,
                        loc.lat,
                    ]
                }
            })

    return jsonify({
        "type": "FeatureCollection",
        "features": data
    })
