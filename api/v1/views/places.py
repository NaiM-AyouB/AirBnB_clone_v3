#!/usr/bin/python3
"""
Flask places
"""

from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """ Retrieves the list of all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = storage.all(Place)
    city_places = []
    for place in all_places.values():
        if place.city_id == city.id:
            city_places.append(place.to_dict())
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place:
        reviews = storage.all(Review)
        for review in reviews.values():
            if review.place_id == place.id:
                storage.delete(review)
        storage.delete(place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_create(city_id):
    """ Creates a Place """
    try:
        city = storage.get(City, city_id)
        if city is None:
            raise ValueError()
        place_dict = request.get_json()
        user = storage.get(User, place_dict['user_id'])
        if user is None:
            raise ValueError()
        place = Place(name=place_dict['name'],
                      city_id=city.id, user_id=user.id)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        if isinstance(ex, KeyError):
            if 'user_id' in str(ex):
                abort(400, 'Missing user_id')
            if 'name' in str(ex):
                abort(400, 'Missing name')
        if isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        print('Exception :')
        print(ex)
        abort(400)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def place_update(place_id):
    """ Updates a Place object """
    try:
        place = storage.get(Place, place_id)
        if place is None:
            raise ValueError()
        place_dict = request.get_json()
        place_dict.pop('id', None)
        place_dict.pop('user_id', None)
        place_dict.pop('city_id', None)
        place_dict.pop('created_at', None)
        place_dict.pop('updated_at', None)
        for key, value in place_dict.items():
            setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict())
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        elif isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        else:
            print('Exception :')
            print(ex)
            abort(400)
