#!/usr/bin/python3
"""Create a new view for place
that handles all default RESTFUL API
actions"""

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def get_places_by_city_id(city_id):
    """This shows places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(
        [place.to_dict() for place in city.places]
    )


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Retrieves a City object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """delete method"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """create a new post req"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")

    user = storage.get(User, data.get("user_id"))
    if user is None:
        abort(404)

    if "name" not in data:
        abort(400, "Missing name")

    new_place = Place(city_id=city.id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            continue

        setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200
