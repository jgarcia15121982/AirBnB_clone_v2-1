#!/usr/bin/python3
"""This module set all the enpoints relataed to cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def cities(state_id=None):
    """This function will show a list with all the cities related to states"""
    found = storage.get(State, state_id)
    if not found:
        abort(404)
    return jsonify([n.to_dict() for n in found.cities])


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def cities_id(city_id=None):
    """This method show a city based on its specific id"""
    city = storage.get(City, city_id)
    if city_id and city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['DELETE'])
def cities_delete(city_id=None):
    """This method delete a city by a given city id"""
    found = storage.get(City, city_id)
    if not found and not city_id:
        abort(404)
    else:
        storage.delete(found)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def city_create(state_id=None):
    """This function will create a city"""
    if not storage.get(State, state_id) and not state_id:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    city = request.get_json()
    city['state_id'] = state_id
    city = City(**city)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['PUT'])
def city_update(city_id=None):
    """This function will update a city"""
    found = storage.get(City, city_id)
    if not found and city_id:
        abort(404)
    else:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        invalid_keys = ["id", "created at", "updated_at", "state_id"]
        for key, value in request.get_json().items():
            key in invalid_keys or setattr(found, key, value)
        found.save()
        return jsonify(found.to_dict()), 200
