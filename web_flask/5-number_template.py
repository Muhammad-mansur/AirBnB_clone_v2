#!/usr/bin/python3
""" 5. Number template """

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Function that returns Hello HBNB """
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Function that returns HBNB """
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """ Function that returns C is fun """
    return "c {}".format(text.replace("_", " "))

@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text="is cool"):
    """ Function that returns Python """
    return "Python {}".format(text.replace("_", " "))

@app.route('/number/<int:n>', strict_slashes=False)
def a_number(n):
    """ Display a number """
    return "{} is a number".format(n)

@app.route('/number_template/<int:n>', strict_slashes=False)
def num_template(n):
    """ render template """
    return render_template('5-number.html', n=n)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)