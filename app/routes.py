from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, RegistrationForm, PostForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Post


@app.route('/', methods=['GET', 'POST'])
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Profile page"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been saved')
        return redirect(url_for('profile'))
    posts = Post.query.all()
    return render_template('profile.html', title='Profile', form=form, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login URL"""
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Welcome')
        return redirect(url_for('profile'))
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration URL"""
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully. Please log in to continue')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    """Used to log out a user"""
    logout_user()
    return redirect(url_for('login'))
