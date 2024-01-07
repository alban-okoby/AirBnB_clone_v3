from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    '''
        Retrieve all Amenity objects
    '''
    amenity_list = [
            amenity.to_dict() for amenity in storage.all(Amenity).values()
            ]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amty_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amty_id):
    '''
        Retrieve one Amenity object
    '''
    amenity = storage.get(Amenity, amty_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<amty_id>', methods=['DELETE'], strict_slashes=False
)
def delete_amenity(amty_id):
    '''
        Delete a Amenity object
    '''
    amenity = storage.get(Amenity, amty_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    '''
        Create a Amenity object
    '''
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amty_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amty_id):
    '''
        Update a Amenity object
    '''
    amenity = storage.get(Amenity, amty_id)
    if amenity is None:
        abort(404)

    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict())
