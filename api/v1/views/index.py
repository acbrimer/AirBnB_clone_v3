#!/usr/bin/python3
"""Module for api/v1 index view"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    return jsonify({"status": "OK"})
