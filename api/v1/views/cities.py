#!/usr/bin/python3
""" RESTful API actions """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False
        )
def get_all_cities(state_id):
    """Retrieve all city objects"""
    try:
        city_list = []
        state_info = storage.get('State', state_id)
        for city in state_info.cities:
            city_dict = city.to_dict()
            city_list.append(city_dict)
        return jsonify(city_list)
    except BaseException:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve one City object"""
    try:
        city = storage.get(City, city_id)
        return jsonify(city.to_dict())
    except Exception:
        abort(404)


@app_views.route('/cities/<ct_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(ct_id):
    """Delete a City object"""
    try:
        city = storage.get(City, ct_id)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False
        )
def post_city(state_id):
    """Create a City object"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    new_city = City(name=request.json['name'], state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'state_id', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
