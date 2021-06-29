#!/usr/bin/python3
"""Module for api/v1 places view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/places', methods=['GET'])
def get_places_list():
    places = [s.to_dict() for s in storage.all(Place).values()]
    return jsonify(places)


@app_views.route('/cities/<string:city_id>/places', methods=['GET'])
def get_places_list_by_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [c.to_dict() for c in city.places]
    if places is None:
        abort(404)
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'])
def get_one_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'])
def delete_one_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places/', methods=['POST'])
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        return "Not a JSON", 400
    place_json = request.get_json()
    if "name" not in place_json:
        return "Missing name", 400
    if "user_id" not in place_json:
        return "Missing user_id", 400
    if storage.get(User, place_json["user_id"]) is None:
        abort(404)
    new_place = Place()
    new_place.__dict__.update(place_json)
    new_place.city_id = city.id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'])
def update_place(place_id):
    if not request.is_json:
        return "Not a JSON", 400
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    for key, val in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, val)
    place.save()
    return place.to_dict(), 200
