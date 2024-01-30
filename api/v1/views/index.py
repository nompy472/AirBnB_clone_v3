#!/usr/bin/python3
"""
Importing Index of the web app
"""
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Fetches all the number of each objects in the db"""
    objects = {k: storage.count(v) for (k, v) in classes.items()}
    return jsonify(objects)
