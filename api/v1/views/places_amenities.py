#!/usr/bin/python3
"""
Views to handle POST, DELETE and GET RESTful API for the link between
Place and Amenity objects
"""
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import make_response, abort, jsonify, request


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """Gets all the amenities of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/api/v1/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Deletes a given amenity from a given place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not (place and amenity):
        abort(404)

    if request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)

        storage.delete_relationship(place, amenity)
        return make_response(jsonify({}), 200)

    else:
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)

        storage.create_relationship(place, amenity)
        return make_response(jsonify(amenity), 201)
