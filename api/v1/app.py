#!/usr/bin/python3
"""Module for api version of AirBnb app"""


from flask import Flask
from os import getenv
from api.v1.views import app_views
import models

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    models.storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),
        port=getenv("HBNB_API_PORT", "5000"))