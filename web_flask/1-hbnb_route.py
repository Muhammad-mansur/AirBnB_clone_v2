#!/usr/bin/python3
""" 1. HBNB """

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """ Function that prints Hello HBNB """
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Function that returns HBNB """
    return "HBNB"


if __name__ == "__main":
    app.run(host="0.0.0.0", port=5000)