#!/usr/bin/python3
"""
    This is RESTful API actions for User objects
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """
    Retrieve all User objects
    """
    user_list = []
    users = storage.all('User').values()
    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """
    Retrieve one User object
    """
    try:
        user = storage.get('User', user_id)
        return jsonify(user.to_dict())
    except Exception:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Delete a User object
    """
    try:
        user = storage.get('User', user_id)
        storage.delete(user)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """
    Create a User object
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(email=request.json.get("email"),
                    password=request.json.get("password"))
    for key, value in request.get_json().items():
        setattr(new_user, key, value)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """
    Update a User object
    """
    obj_user = storage.get('User', user_id)
    if obj_user is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'email', 'updated_at']:
            setattr(obj_user, key, value)
    obj_user.save()
    return jsonify(obj_user.to_dict()), 200
