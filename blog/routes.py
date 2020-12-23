from flask import render_template, url_for, flash, redirect, request, send_from_directory-
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post
from blog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
import os


postsdic = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog post 1',
        'content': 'first post content',
        'date_posted': 'April 20,2018'
    },
    {
        'author': 'Schena Francesco',
        'title': 'Blog post 2',
        'content': 'second post content',
        'date_posted': 'April 24,2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=postsdic)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Nope, try again', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
