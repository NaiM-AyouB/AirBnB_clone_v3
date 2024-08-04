#!/usr/bin/python3
"""
Flask API
"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS, cross_origin

# Global Flask Application (app)
app = Flask(__name__)

# global jsonify prettier
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# global strict slashes
app.url_map.strict_slashes = False

# get environment variables
HBNB_API_HOST = getenv("HBNB_API_HOST") or '0.0.0.0'
HBNB_API_PORT = getenv("HBNB_API_PORT") or '5000'

# Cross-Origin Resource Sharing
cors = CORS(app, resources={r'/*': {'origins': HBNB_API_HOST}})

# app_views register blueprint
app.register_blueprint(app_views)


# close db after requests
@app.teardown_appcontext
def close_storage(exception):
    """ after each request, this method calls storage.close() """
    storage.close()


# 404 errors handlers
@app.errorhandler(404)
def page_not_found(error):
    """ return Not found """
    response = {"error": "Not found"}
    return jsonify(response), 404


if __name__ == '__main__':
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
