#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """GET"""
    return jsonify([n.to_dict() for n in storage.all(State).values()])


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def states_id(state_id):
    """GET with state_id"""
    found = storage.get(State, state_id)
    if not found:
        abort(404)
    else:
        return jsonify(found.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def states_delete(state_id):
    """DELETE"""
    found = storage.get(State, state_id)
    if not found:
        abort(404)
    else:
        storage.delete(found)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def states_create():
    """POST"""
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def states_update(state_id):
    """PUT"""
    found = storage.get(State, state_id)
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
