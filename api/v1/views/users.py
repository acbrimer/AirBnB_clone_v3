#!/usr/bin/python3
"""Module for api/v1 amenities view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users_list():
    users = [s.to_dict() for s in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'])
def delete_one_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'])
def create_user():
    if not request.is_json:
        return "Not a JSON", 400
    amenity_json = request.get_json()
    if "name" not in amenity_json:
        return "Missing name", 400
    new_user = User()
    new_user.__dict__.update(amenity_json)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    if not request.is_json:
        return "Not a JSON", 400
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    for key, val in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, val)
    user.save()
    return user, 200
