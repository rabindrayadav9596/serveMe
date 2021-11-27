from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Service, Provider, Order
from flask_login import login_required, current_user
from sqlalchemy import *
import datetime
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/provider_profile')
@login_required
def provider_profile():
    return render_template('provider_profile.html', user=current_user)




