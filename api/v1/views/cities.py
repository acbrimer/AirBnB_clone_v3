#!/usr/bin/python3
"""Module for api/v1 cities view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/cities', methods=['GET'])
def get_cities_list():
    cities = [s.to_dict() for s in storage.all(City).values()]
    return jsonify(cities)


@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def get_cities_list_by_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [c.to_dict() for c in state.cities]
    if cities is None:
        abort(404)
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def get_one_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_one_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        return "Not a JSON", 400
    city_json = request.get_json()
    if "name" not in city_json:
        return "Missing name", 400
    new_city = City()
    new_city.__dict__.update(city_json)
    new_city.state_id = state.id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>/', methods=['PUT'])
def update_city(city_id):
    if not request.is_json:
        return "Not a JSON", 400
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if 'id' in data:
        del(data['id'])
    if 'created_at' in data:
        del(data['created_at'])
    if 'updated_at' in data:
        del(data['updated_at'])
    for key, val in data.items():
        setattr(city, key, val)
    storage.save()
    return city, 200
