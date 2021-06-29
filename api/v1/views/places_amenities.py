#!/usr/bin/python3
"""Module for api/v1 places_amenities view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [c.to_dict() for c in place.amenities]
    if amenities is None:
        abort(404)
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>', methods=['DELETE'])
def delete_one_review(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    storage.save()
    storage.reload()
    return jsonify({}), 200
