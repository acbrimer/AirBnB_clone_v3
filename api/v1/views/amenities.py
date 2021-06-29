#!/usr/bin/python3
"""Module for api/v1 amenities view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities_list():
    amenities = [s.to_dict() for s in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'])
def get_one_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'])
def delete_one_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    if not request.is_json:
        return "Not a JSON", 400
    amenity_json = request.get_json()
    if "name" not in amenity_json:
        return "Missing name", 400
    new_amenity = Amenity()
    new_amenity.__dict__.update(amenity_json)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    if not request.is_json:
        return "Not a JSON", 400
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if 'id' in data:
        del(data['id'])
    if 'created_at' in data:
        del(data['created_at'])
    if 'updated_at' in data:
        del(data['updated_at'])
    for key, val in data.items():
        setattr(amenity, key, val)
    storage.save()
    storage.reload()
    return amenity, 200
