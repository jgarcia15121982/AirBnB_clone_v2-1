#!/usr/bin/python3
"""app module"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.teardown_appcontext
def clse(self):
    """docs"""
    storage.close()


@app.errorhandler(404)
def page_not_fount(e):
    """Page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    """docs"""
    hst = getenv('HBNB_API_HOST')
    prt = getenv('HBNB_API_PORT')
    if hst is None:
        hst = '0.0.0.0'
    if prt is None:
        prt = 5000
    app.run(host=hst, port=prt, threaded=True, debug=True)
