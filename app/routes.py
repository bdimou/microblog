"""
The routes are the different URLs that the application implements. In Flask, handlers for the application routes are written as Python functions, called <i> view functions </i>.
View functions are mapped to one or more routes URLs so that Flask knows what logic to execute when a client requests a given URL.
"""

from flask import render_template, redirect, flash, url_for
from app import app
from app.forms import LoginForm


@app.route('/')                # A decorator modifies the function that follows it. A common pattern with decorators is to use them to register functions as callbacks for certain events
@app.route('/index')           # In this case, the @app.route decorator creates an association between the URL given as an argument and the function 
def index():
    user = {'username':'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',title='Home',user=user,posts=posts) # this will call Jinja2 (template engine) to handle dynamic content placeholders
    

@app.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data,form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign In',form=form)