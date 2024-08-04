#!/usr/bin/python3
"""
Flask cities
"""

from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = storage.all('City')
    state_cities = []
    for city in all_cities.values():
        if city.state_id == state.id:
            state_cities.append(city.to_dict())
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city:
        places = storage.all(Place)
        for place in places.values():
            if place.city_id == city.id:
                reviews = storage.all(Review)
                for review in reviews.values():
                    if review.place_id == place.id:
                        storage.delete(review)
                storage.delete(place)
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_create(state_id):
    """ Creates a City """
    try:
        state = storage.get(State, state_id)
        if state is None:
            raise ValueError()
        city_dict = request.get_json()
        city = City(name=city_dict['name'], state_id=state_id)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        elif isinstance(ex, KeyError):
            abort(400, 'Missing name')
        elif isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        else:
            print('Exception :')
            print(ex)
            abort(400)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def city_update(city_id):
    """ Updates a City object """
    try:
        city = storage.get(City, city_id)
        if city is None:
            raise ValueError()
        city_dict = request.get_json()
        city_dict.pop('id', None)
        city_dict.pop('state_id', None)
        city_dict.pop('created_at', None)
        city_dict.pop('updated_at', None)
        for key, value in city_dict.items():
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict())
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        if isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        print('Exception :')
        print(ex)
        abort(400)
