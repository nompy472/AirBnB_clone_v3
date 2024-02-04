#!/usr/bin/python3
"""
Views that handle all the default RESTful API for Amenity Resource
"""
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import render_template, abort, jsonify, request


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenities(place_id):
    """Gets all the amenities of a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)
