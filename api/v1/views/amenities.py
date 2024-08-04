#!/usr/bin/python3
"""
Flask amenities
"""

from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities():
    """ Retrieves the list of all Amenity objects """
    all_amenities = storage.all(Amenity)
    all_amenities = list(
        amenity.to_dict() for amenity in all_amenities.values())
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def amenity_create():
    """ Creates a Amenity """
    try:
        amenity_dict = request.get_json()
        amenity = Amenity(name=amenity_dict['name'])
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    except Exception as ex:
        if isinstance(ex, KeyError):
            abort(400, 'Missing name')
        if isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        print('Exception :')
        print(ex)
        abort(400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """ Updates a Amenity object """
    try:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            raise ValueError()
        amenity_dict = request.get_json()
        amenity_dict.pop('id', None)
        amenity_dict.pop('created_at', None)
        amenity_dict.pop('updated_at', None)
        for key, value in amenity_dict.items():
            setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict())
    except Exception as ex:
        if isinstance(ex, ValueError):
            abort(404)
        elif isinstance(ex, BadRequest):
            abort(400, 'Not a JSON')
        else:
            print('Exception :')
            print(ex)
            abort(400)
