#!/usr/bin/python3
"""
Flask users
"""

from http.client import HTTPException
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def users():
    """ Retrieves the list of all User objects """
    all_users = storage.all(User)
    all_users = list(user.to_dict() for user in all_users.values())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user:
        places = storage.all(Place)
        reviews = storage.all(Review)
        for place in places.values():
            if place.user_id == user.id:
                storage.delete(place)
        for review in reviews.values():
            if review.user_id == user.id:
                storage.delete(review)
        storage.delete(user)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def user_create():
    """ Creates a User """
    try:
        user_dict = request.get_json()
        user = User(email=user_dict['email'], password=user_dict['password'])
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201
    except Exception as ex:
        if isinstance(ex, KeyError):
            if 'email' in str(ex):
                abort(400, 'Missing email')
            if 'password' in str(ex):
                abort(400, 'Missing password')
        if isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        print('Exception :')
        print(ex)
        abort(400)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def user_update(user_id):
    """ Updates a User object """
    try:
        user = storage.get(User, user_id)
        if user is None:
            raise ValueError()
        user_dict = request.get_json()
        user_dict.pop('id', None)
        user_dict.pop('created_at', None)
        user_dict.pop('updated_at', None)
        for key, value in user_dict.items():
            setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict())
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        elif isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        else:
            print('Exception :')
            print(ex)
            abort(400)
