#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def user():
    """GET"""
    return jsonify([n.to_dict() for n in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user_id(user_id):
    """GET with state_id"""
    found = storage.get(User, user_id)
    if not found:
        abort(404)
    else:
        return jsonify(found.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """DELETE"""
    found = storage.get(User, user_id)
    if not found:
        abort(404)
    else:
        storage.delete(found)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def user_create():
    """POST"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in request.get_json():
        return jsonify({"error": "Missing email"}), 400
    if "password" not in request.get_json():
        return jsonify({"error": "Missing password"}), 400
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def user_update(user_id):
    """PUT"""
    found = storage.get(User, user_id)
    if not found:
        abort(404)
    else:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        invalid_keys = ["id", "created at", "updated_at", "email"]
        for key, value in request.get_json().items():
            key in invalid_keys or setattr(found, key, value)
        found.save()
    return jsonify(found.to_dict()), 200
