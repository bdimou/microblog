"""
The routes are the different URLs that the application implements. In Flask, handlers for the application routes are written as Python functions, called <i> view functions </i>.
View functions are mapped to one or more routes URLs so that Flask knows what logic to execute when a client requests a given URL.
"""

from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, Worlds"
