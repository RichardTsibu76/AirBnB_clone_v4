#!/usr/bin/python3

"""
This module contains the routes and functions for managing cities in the API.

Routes:
    - /states/<state_id>/cities [GET]: Retrieve all cities associated with a
    given state.
    - /cities/<city_id> [GET]: Retrieve a city by its ID.
    - /cities/<city_id> [DELETE]: Delete a city based on its ID.
    - /states/<state_id>/cities [POST]: Create a new city for a given state.
    - /cities/<city_id> [PUT]: Update a city with the given city_id.

Functions:
    - get_cities_by_state(state_id): Retrieve all cities associated with a
    given state.
    - get_city_by_id(city_id): Retrieve a city by its ID.
    - delete_city(city_id): Delete a city based on its ID.
    - create_city(state_id): Create a new city for a given state.
    - update_city(city_id): Update a city with the given city_id.
"""

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities_by_state(state_id):
    """
    Retrieve all cities associated with a given state.

    Args:
        state_id (str): The ID of the state.

    Returns:
        JSON: A JSON response containing a list of dictionaries representing
        the cities.

    Raises:
        404: If the state with the given ID does not exist.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city_by_id(city_id):
    """
    Retrieve a city by its ID.

    Args:
        city_id (str): The ID of the city to retrieve.

    Returns:
        dict: A JSON representation of the city.

    Raises:
        404: If the city with the specified ID does not exist.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
    Delete a city based on its ID.

    Args:
        city_id (str): The ID of the city to be deleted.

    Returns:
        tuple: A tuple containing an empty JSON response and a status code of
        200.

    Raises:
        404: If the city with the specified ID does not exist.
    """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """
    Create a new city for a given state.

    Args:
        state_id (str): The ID of the state for which the city is
        being created.

    Returns:
        dict: A JSON representation of the newly created city.

    Raises:
        404: If the state with the given ID does not exist.
        400: If the request data is not a valid JSON or if the 'name' field is
        missing.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json(force=True, silent=True)

    if not data:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    new_city = City(state_id=state.id, **data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """
    Update a city with the given city_id.

    Args:
        city_id (str): The ID of the city to be updated.

    Returns:
        tuple: A tuple containing the JSON representation of the updated city
        and the HTTP status code.

    Raises:
        404: If the city with the given city_id does not exist.
        400: If the request data is not a valid JSON or if the 'name' field is
        missing.
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")

    if "name" not in data:
        abort(400, "Missing name")

    for key, value in data.items():
        if key in ['id', 'created_at', 'updated_at', 'state_id']:
            continue

        setattr(city_obj, key, value)

    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
