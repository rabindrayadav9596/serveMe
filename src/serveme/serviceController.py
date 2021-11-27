

from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import Service, Provider
from flask_login import login_required, current_user

from sqlalchemy import *




serviceController = Blueprint('serviceController', __name__)

@serviceController.route('/services')
def services():
    result = "no data found"
    service= request.args.get('service');
    if service=='appliances':
        result = Service.query.filter_by(category="Appliances").all()
    elif service=='electrical':
        result = Service.query.filter_by(category="Electrical").all()
    elif service=='plumbing':
        result = Service.query.filter_by(category="Plumbing").all()
    elif service=='cleaning':
        result = Service.query.filter_by(category="Cleaning").all()
    elif service=='tutoring':
        result = Service.query.filter_by(category="Tutoring").all()
    elif service=='moving':
        result = Service.query.filter_by(category="Moving").all()
    elif service=='computer':
        result = Service.query.filter_by(category="Computer").all()
    elif service=='painting':
        result = Service.query.filter_by(category="Painting").all()
    elif service=='pest_control':
        result = Service.query.filter_by(category="Pest Control").all()
    return render_template('services.html', result=result, serv = service)

@serviceController.route('/view_services')
def view_services():
    
    provider = Provider.query.filter_by(userID = current_user.userID).first()
    provider_id = provider.provider_id
   
    services = Service.query.filter_by(provider_id = provider_id )

    return render_template('view_services.html', services = services)

@serviceController.route('/add_service')
def add_service():
    return render_template('add_service.html', services = services)

@serviceController.route('/add_service', methods=['POST'])
def add_service_post():

    provider = Provider.query.filter_by(userID = current_user.userID).first()
    provider_id = provider.provider_id
    service_name = request.form.get('service_name')
    cost = request.form.get('cost')
    description = request.form.get('description')
    category = request.form.get('category')


    # new_user = User( userID=userID, email=email, name=name, password=generate_password_hash(password, method='sha256'),gender=gender,age=age, phoneNum=phoneNum, points=points, type='customer')
    service = Service(provider_id = provider_id, rating_avg = 3.0, service_name = service_name, cost = cost, description = description, category=category)
    # add the new user to the database
    db.session.add(service)
    db.session.commit()

    services = Service.query.filter_by(provider_id = provider_id )

    return redirect(url_for('serviceController.view_services', services = services))