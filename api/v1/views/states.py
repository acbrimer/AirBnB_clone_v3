#!/usr/bin/python3
"""Module for api/v1 states view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states_list():
    states = [s.to_dict() for s in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_one_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_one_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def create_state():
    if not request.is_json:
        return "Not a JSON", 400
    state_json = request.get_json()
    if "name" not in state_json:
        return "Missing name", 400
    new_state = State()
    new_state.__dict__.update(state_json)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    if not request.is_json:
        return "Not a JSON", 400
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if 'id' in data:
        del(data['id'])
    if 'created_at' in data:
        del(data['created_at'])
    if 'updated_at' in data:
        del(data['updated_at'])
    state.__dict__.update(data)
    state.save()
    return state, 200
