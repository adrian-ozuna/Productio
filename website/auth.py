from flask import Blueprint, get_flashed_messages, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        rememberSession = False

        if request.form.get('rememberMe'):
            rememberSession = True

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=rememberSession)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email doesn\'t exist', category='error')
    
    if not current_user.is_authenticated:
        return render_template("login.html", user = current_user)
    else:
        return redirect(url_for("views.home"))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        userEmailChecker = User.query.filter_by(email = email).first()
        userUsernameChecker = User.query.filter_by(username = username).first()

        if userEmailChecker:
            flash('Email address is already in use.', category='error')

        if userUsernameChecker:
            flash('Username is already in use', category='error')

        if len(email) < 3:
            flash('Email length must be greater than 3 characters', category='error')
        if len(username) < 5:
            flash('Username length must be greater than 5 characters', category='error')
        if len(password) < 8:
            flash('Password length must be greater than 8 characters', category='error')
        if password != passwordConfirm:
            flash('Passwords don\'t match', category='error')

        messages = get_flashed_messages(with_categories = True)
        
        if len(messages) == 0:
            new_user = User(email = email, username = username, password = generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))

    if not current_user.is_authenticated:
        return render_template("signup.html", user = current_user)
    else:
        return redirect(url_for("views.home"))