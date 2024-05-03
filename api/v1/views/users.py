#!/usr/bin/python3
"""Creating new view for user  objects
that handles all default RESTFul
API actions"""

from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users")
@app_views.route("/users/<user_id>")
def get_users(user_id=None):
    """
    Retrieve user(s) information.

    Args:
        user_id (str): Optional. The ID of the user to retrieve.

    Returns:
        If user_id is None:
            A JSON response containing a list of dictionaries, each
            representing a user.
        If user_id is provided:
            A JSON response containing the information of the specified user.

    Raises:
        404: If the user with the specified user_id is not found.
    """
    if user_id is None:
        return jsonify(
            [user.to_dict() for user in storage.all(User).values()]
        )

    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    return jsonify(user_obj.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user by user_id.

    Args:
        user_id (str): The ID of the user to be deleted.

    Returns:
        tuple: A tuple containing an empty JSON response and a status code of
        200.

    Raises:
        404: If the user with the specified user_id is not found.
    """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
def create_user():
    """
    Create a new user.

    This endpoint allows the creation of a new user by providing the required
    information in the request body as a JSON object. The JSON object should
    contain the following fields:
    - email: The email address of the user.
    - password: The password for the user.

    Returns:
        A JSON response containing the newly created user's information and
        a status code of 201 (Created) if the user was successfully created.

    Raises:
        400 (Bad Request): If the request body is not a valid JSON object or
        if any of the required fields (email, password) are missing.
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")

    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update a user with the given user_id.

    Args:
        user_id (str): The ID of the user to be updated.

    Returns:
        tuple: A tuple containing the JSON representation of the updated user
        and the HTTP status code.

    Raises:
        404: If the user with the given user_id does not exist.
        400: If the request data is not a valid JSON.

    """
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)

    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key in ['id', 'email', 'created_at', 'updated_at']:
            continue

        setattr(user_obj, key, value)

    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
