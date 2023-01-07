"""
The routes are the different URLs that the application implements. In Flask, handlers for the application routes are written as Python functions, called <i> view functions </i>.
View functions are mapped to one or more routes URLs so that Flask knows what logic to execute when a client requests a given URL.
"""

from flask import render_template, redirect, flash, url_for, request,g, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import get_locale
from werkzeug.urls import url_parse
from datetime import datetime
from app import app,db
from app.forms import LoginForm, RegistrationForm,EditProfileForm, EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User,Post
from app.email import send_password_reset_email
from app.translate import translate
from langdetect import detect, LangDetectException


@app.route('/', methods =['GET','POST'])                # A decorator modifies the function that follows it. A common pattern with decorators is to use them to register functions as callbacks for certain events
@app.route('/index',methods =['GET','POST'])            # In this case, the @app.route decorator creates an association between the URL given as an argument and the function 
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        try:
            language = detect(form.post.data) 
        except LangDetectException:
            language=''
        post = Post(body=form.post.data, author=current_user, language = language)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))               # Post/Redirect/Get pattern. It avoids inserting posts when a user inadvertently refreshes the pages after submitting a web form.
    page = request.args.get('page',1,type =int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out = False)
    next_url = url_for('index',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index',page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',title='Home',form=form, posts=posts.items,next_url = next_url, prev_url = prev_url) # this will call Jinja2 (template engine) to handle dynamic content placeholders
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>') # dynamic component <>
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page,per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    form = EmptyForm()
    next_url = url_for('user',username = user.username, page= posts.next_num) if posts.has_next else None
    prev_url = url_for('user',username= user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html',user=user,posts=posts.items,next_url=next_url, prev_url =prev_url,form=form)

@app.route('/edit_profile', methods =['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET': # research that a bit more
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('explore',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore',page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',title='Explore',posts=posts.items,next_url = next_url, prev_url=prev_url)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      'EN-US' if request.form['source_language']=='en' else request.form['source_language'],
                                      request.form['dest_language'])})

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    g.locale = str(get_locale())
    if g.locale == 'en':
        g.locale = 'EN-US'

