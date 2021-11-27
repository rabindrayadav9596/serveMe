from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Provider
from . import db
import uuid

loginController = Blueprint('loginController', __name__)

@loginController.route('/login')
def login():
    return render_template('login.html')

@loginController.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash("User doesn't exist or password is incorrect" )
        return redirect(url_for('loginController.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    if user.type == "customer":
        return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('main.provider_profile'))