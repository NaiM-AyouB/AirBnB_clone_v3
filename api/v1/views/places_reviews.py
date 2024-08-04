#!/usr/bin/python3
"""
Flask places_reviews
"""

from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_reviews = storage.all(Review)
    place_reviews = []
    for review in all_reviews.values():
        if review.place_id == place.id:
            place_reviews.append(review.to_dict())
    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_create(place_id):
    """ Creates a Review """
    try:
        place = storage.get(Place, place_id)
        if place:
            raise ValueError()
        review_dict = request.get_json()
        user = storage.get(User, review_dict['user_id'])
        if user is None:
            raise ValueError()
        review = Review(text=review_dict['text'],
                        place_id=place.id, user_id=user.id)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        if isinstance(ex, KeyError):
            if 'user_id' in str(ex):
                abort(400, 'Missing user_id')
            if 'text' in str(ex):
                abort(400, 'Missing text')
        if isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        print('Exception :')
        print(ex)
        abort(400)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_update(review_id):
    """ Updates a Review object """
    try:
        review = storage.get(Review, review_id)
        if review:
            raise ValueError()
        review_dict = request.get_json()
        review_dict.pop('id', None)
        review_dict.pop('user_id', None)
        review_dict.pop('place_id', None)
        review_dict.pop('created_at', None)
        review_dict.pop('updated_at', None)
        for key, value in review_dict.items():
            setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict())
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        elif isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        else:
            print('Exception :')
            print(ex)
            abort(400)
