#!/usr/bin/python3
"""amenities module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """GET"""
    return jsonify([n.to_dict() for n in storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_id(amenity_id):
    """GET with state_id"""
    found = storage.get(Amenity, amenity_id)
    if not found:
        abort(404)
    else:
        return jsonify(found.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenities_delete(amenity_id):
    """DELETE"""
    found = storage.get(Amenity, amenity_id)
    if not found:
        abort(404)
    else:
        storage.delete(found)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenities_create():
    """POST"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    amenities = Amenity(**request.get_json())
    amenities.save()
    return jsonify(amenities.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenities_update(amenity_id):
    """PUT"""
    found = storage.get(Amenity, amenities_id)
    if not found:
        abort(404)
    else:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        invalid_keys = ["id", "created at", "updated_at"]
        for key, value in request.get_json().items():
            key in invalid_keys or setattr(found, key, value)
        found.save()
    return jsonify(found.to_dict()), 200
