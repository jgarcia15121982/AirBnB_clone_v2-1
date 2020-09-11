#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models import storage
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review(place_id):
    """Create places acording to the city"""
    found = storage.get(Place, place_id)
    if not found:
        abort(404)
    return jsonify([n.to_dict() for n in found.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review_id(review_id):
    """This function shows all places"""
    found = storage.get(Review, review_id)
    if not found:
        abort(404)
    else:
        return jsonify(found.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """Delete the place specified by the id"""
    found = storage.get(Review, review_id)
    if not found:
        abort(404)
    else:
        storage.delete(found)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_create(place_id):
    """Create a place acording to the  city"""
    found = storage.get(Place, place_id)
    if not found:
        abort(404)
    else:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        if "user_id" not in request.get_json():
            return jsonify({"error": "Missing user_id"}), 400

        user = storage.get(User, request.get_json()['user_id'])
        if not user:
            abort(404)

        if "text" not in request.get_json():
            return jsonify({"error": "Missing text"}), 400

        review = request.get_json()
        review['place_id'] = place_id
        review = Review(**review)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_update(review_id):
    """Updates a place acording to the place"""
    found = storage.get(Review, review_id)
    print(found)
    if not found:
        abort(404)
    else:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        invalid_keys = ["id", "user_id", "created at", "updated_at"]
        for key, value in request.get_json().items():
            key in invalid_keys or setattr(found, key, value)
        found.save()
        return jsonify(found.to_dict()), 200
