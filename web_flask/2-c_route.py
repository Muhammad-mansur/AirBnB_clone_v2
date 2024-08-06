#!/usr/bin/python3
""" 2. C is fun """

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

@app.route("/c/<text>", strict_slashes=False)
def c_is_fun(text):
    """ Function that returns C is fun """
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main":
    app.run(host="0.0.0.0", port=5000)