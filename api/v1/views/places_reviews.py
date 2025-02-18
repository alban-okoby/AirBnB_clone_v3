#!/usr/bin/python3
"""
RESTful API actions for user object
"""
from flask import jsonify, make_response, abort, request, Blueprint
from api.v1.views import app_views
from models import storage
from models import Review, Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews_list = []
    for review in storage.all("Review").values():
        if review.place_id == place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """
    Retrieve one review object
    """
    try:
        review = storage.get('Review', review_id)
        return jsonify(review.to_dict())
    except Exception:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Delete a review object
    """
    try:
        review_obj = storage.get('Review', review_id)
        storage.delete(review_obj)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """
    Create a review object
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in request.json:
        return jsonify({"error": "Missing user_id"}), 400
    new_review = Review(user_id=request.json["user_id"], place_id=place_id)
    for key, value in request.json.items():
        setattr(new_review, key, value)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """
    Update a review object
    """
    obj_review = storage.get('Review', review_id)
    if obj_review is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'user_id', 'updated_at']:
            setattr(obj_review, key, value)
    obj_review.save()
    return jsonify(obj_review.to_dict()), 200
