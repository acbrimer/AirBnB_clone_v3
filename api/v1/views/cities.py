#!/usr/bin/python3
"""Module for api/v1 cities view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/cities', methods=['GET'])
def get_list():
    cities = [s.to_dict() for s in storage.all(City).values()]
    return jsonify(cities)


@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def get_list_by_state(state_id):
    cities = [c.to_dict() for c in storage.get(State, state_id).cities.values()]
    if cities is None:
        abort(404)
    return jsonify(cities.to_dict())

@app_views.route('/cities/<string:city_id>', methods=['GET'])
def get_one(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_one(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'])
def create(state_id):
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
    new_city.state = state
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>/', methods=['PUT'])
def update(city_id):
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
    city.__dict__.update(data)
    city.save()
    return city, 200
