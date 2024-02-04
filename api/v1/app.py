#!/usr/bin/python3
"""
Web application that provides the API for the project
"""
from models import storage
from api.v1.views import app_views
from os import environ
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def close_db(error):
    """Closes the Storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 Error
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5050'
    app.run(host=host, port=port, threaded=True)
