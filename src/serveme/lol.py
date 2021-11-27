from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Service, PastOrder
from flask_login import login_required, current_user


main = Blueprint('main', __name__)


@main.route('/')	
def index():
    return render_template('index.html')


@main.route('/categories', methods=['POST'])
@login_required
def category_post():
    result = 0
    if request.form.get("appliancesBtn"):
        result = Service.query.filter_by(category="Appliances").limit(20).all()
    elif request.form.get("electricalBtn"):
        result = Service.query.filter_by(category="Electrical").limit(20).all()
    elif request.form.get("plumbingBtn"):
        result = Service.query.filter_by(category="Plumbing").limit(20).all()
    elif request.form.get("cleaningBtn"):
        result = Service.query.filter_by(category="HomeCleaning").limit(20).all()
    elif request.form.get("tutoringBtn"):
        result = Service.query.filter_by(category="Tutoring").limit(20).all()
    elif request.form.get("packagingBtn"):
        result = Service.query.filter_by(category="Packaging").limit(20).all()
    elif request.form.get("computerBtn"):
        result = Service.query.filter_by(category="Computer Repair").limit(20).all()
    elif request.form.get("homerepairBtn"):
        result = Service.query.filter_by(category="Home Repair").limit(20).all()
    elif request.form.get("pestBtn"):
        result = Service.query.filter_by(category="Pest Control").limit(20).all()
    return render_template('result.html', result=result)

@main.route('/profile')
@login_required
def profile():
    pastOrders= PastOrder.query.filter_by(userID=current_user.userID).all()
    #points= 
    return render_template('profile.html', name=current_user.name)
