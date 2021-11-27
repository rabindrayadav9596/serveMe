from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Provider
from . import db
import uuid

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash("User doesn't exist or password is incorrect" )
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    if user.type == "customer":
        return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('main.provider_profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    gender = request.form.get('gender')
    age = request.form.get('age')
    phoneNum = request.form.get('phoneNum')
    userID= uuid.uuid4().hex
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    points = 0

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the    plaintext version isn't saved.
    # gender=gender, age=age, phone_number=phone_number
    new_user = User( userID=userID, email=email, name=name, password=generate_password_hash(password, method='sha256'),gender=gender,age=age, phoneNum=phoneNum, points=points, type='customer')
   
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/service_provider_signup')
def service_provider_signup():
    return render_template('signup_service_provider.html')

@auth.route('/service_provider_signup', methods=['POST'])
def service_provider_signup_post():
    email = request.form.get('email')
    provider_name = request.form.get('name')
    password = request.form.get('password')
    gender = request.form.get('gender')
    age = request.form.get('age')
    phoneNum = request.form.get('phoneNum')
    address = request.form.get('address')
    ssn = request.form.get('ssn')
    userID= uuid.uuid4().hex
   
    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    points = 0

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.service_provider_signup'))

    # create a new user with the form data. Hash the password so the    plaintext version isn't saved.
    # gender=gender, age=age, phone_number=phone_number
    new_user = User( userID=userID, email=email, name=provider_name, password=generate_password_hash(password, method='sha256'),gender=gender,age=age, phoneNum=phoneNum, points=points, type='provider')
    
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.create_provider', userID = userID, provider_name = provider_name, phone_number = phoneNum, address = address, email = email, ssn = ssn))
    

@auth.route('/create_provider')
def create_provider():
    userID = request.args.get('userID')
    provider_name = request.args.get('provider_name')
    phone_number = request.args.get('phone_number')
    address = request.args.get('address')
    email = request.args.get('email')
    ssn = request.args.get('ssn')

    provider = Provider( provider_name=provider_name, userID = userID, rating_avg = 3.0, phone_number = phone_number, address = address, email = email, ssn = ssn)
    db.session.add(provider)
    db.session.commit()
    return redirect(url_for('auth.login'))

