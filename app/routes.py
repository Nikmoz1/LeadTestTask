import random
from flask_track_usage import TrackUsage
from flask_track_usage.storage.printer import PrintWriter
from flask_track_usage.storage.output import OutputWriter

from flask import render_template, flash, redirect, url_for, request, make_response, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User

def my_
@app.route('/')
@app.route('/index')
@login_required
def index():
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
    return render_template('index.html', title='Home', posts=posts)


@app.route('/get-cookie/')
def get_cookie():
    username = request.cookies.get('somecookiename')
    print(username)
    return render_template('test.html')


@app.route('/cookie/')
def cookie():
    res = make_response("Setting a cookie")
    id_ = random.randint(1, 100)
    res.set_cookie('id', str(id_), max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not request.cookies.get("id"):
        res = make_response()
        id_ = random.randint(1, 100)
        res.set_cookie('id', str(id_), max_age=60 * 60 * 24 * 365 * 2)
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
            next_page = url_for('index')
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
