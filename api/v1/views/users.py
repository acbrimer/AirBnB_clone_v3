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
def delete_one_amenity(user_id):
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
    if 'id' in data:
        del(data['id'])
    if 'created_at' in data:
        del(data['created_at'])
    if 'updated_at' in data:
        del(data['updated_at'])
    for key, val in data.items():
        setattr(user, key, val)
    storage.save()
    storage.reload()
    return user, 200
