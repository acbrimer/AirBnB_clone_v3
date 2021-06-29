#!/usr/bin/python3
"""Module for api/v1 reviews view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/reviews', methods=['GET'])
def get_reviews_list():
    reviews = [s.to_dict() for s in storage.all(Review).values()]
    return jsonify(reviews)


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'])
def get_reviews_list_by_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [c.to_dict() for c in place.reviews]
    if reviews is None:
        abort(404)
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'])
def get_one_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'])
def delete_one_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews/', methods=['POST'])
def create_review(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        return "Not a JSON", 400
    review_json = request.get_json()
    if "user_id" not in review_json:
        return "Missing user_id", 400
    if storage.get(User, review_json["user_id"]) is None:
        abort(404)
    if "text" not in review_json:
        return "Missing text", 400
    new_review = Review()
    new_review.__dict__.update(review_json)
    new_review.place_id = place.id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'])
def update_review(review_id):
    if not request.is_json:
        return "Not a JSON", 400
    reviwe = storage.get(Review, review_id)
    if reviwe is None:
        abort(404)
    data = request.get_json()
    for key, val in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(reviwe, key, val)
    reviwe.save()
    return reviwe.to_dict(), 200
