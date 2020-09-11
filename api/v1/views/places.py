#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models import storage
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places(city_id):
    """Create places acording to the city"""
    found = storage.get(City, city_id)
    print(found)
    if not found:
        abort(404)
    return jsonify([n.to_dict() for n in found.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def places_id(place_id):
    """This function shows all places"""
    found = storage.get(Place, place_id)
    if not found:
        abort(404)
    else:
        return jsonify(found.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def places_delete(place_id):
    """Delete the place specified by the id"""
    found = storage.get(Place, place_id)
    if not found:
        abort(404)
    else:
        storage.delete(found)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def places_create(city_id):
    """Create a place acording to the  city"""
    found = storage.get(City, city_id)
    if not found:
        abort(404)
    else:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        elif "user_id" not in request.get_json():
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get(User, request.get_json()['user_id'])
        if not user:
            abort(404)
        if "name" not in request.get_json():
            return jsonify({"error": "Missing name"}), 400
        place = request.get_json()
        place['city_id'] = city_id
        place = Place(**place)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def places_update(place_id):
    """Updates a place acording to the place"""
    found = storage.get(Place, place_id)
    if not found:
        abort(404)
    else:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        invalid_keys = ["id", "user_id", "city_id", "created at", "updated_at"]
        for key, value in request.get_json().items():
            key in invalid_keys or setattr(found, key, value)
        found.save()
        return jsonify(found.to_dict()), 200
