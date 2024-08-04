#!/usr/bin/python3
"""
Flask states
"""

from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    all_states = storage.all(State)
    all_states = list(state.to_dict() for state in all_states.values())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def state(state_id):
    """ Retrieves a State object """
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """ Deletes a State object """
    state = storage.get('State', state_id)
    if state:
        cities = storage.all(City)
        for city in cities.values():
            if city.state_id == state.id:
                places = storage.all(Place)
                for place in places.values():
                    if place.city_id == city.id:
                        reviews = storage.all(Review)
                        for review in reviews.values():
                            if review.place_id == place.id:
                                storage.delete(review)
                        storage.delete(place)
                storage.delete(city)
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def state_create():
    """ Creates a State """
    try:
        state_dict = request.get_json()
        state = State(name=state_dict['name'])
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201
    except Exception as ex:
        if isinstance(ex, KeyError):
            abort(400, 'Missing name')
        if isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        print('Exception :')
        print(ex)
        abort(400)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def state_update(state_id):
    """ Updates a State object """
    try:
        state = storage.get('State', state_id)
        if state is None:
            raise ValueError()
        state_dict = request.get_json()
        state_dict.pop('id', None)
        state_dict.pop('created_at', None)
        state_dict.pop('updated_at', None)
        for key, value in state_dict.items():
            setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        elif isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        else:
            print('Exception :')
            print(ex)
            abort(400)
