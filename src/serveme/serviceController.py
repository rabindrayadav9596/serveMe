

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
    name = request.args.get('name')
    address = request.args.get('address')
    stars = request.args.get('stars')
    providers = None
    result = None
    #if all name, address, and stars are null
   
    providers = Provider.query.all()

    #if only name is present
    if name and not address and not stars:
        providers = Provider.query.filter(Provider.provider_name.like("%"+name+"%")).all()
        
    elif address and not name and not stars:
        providers = Provider.query.filter(Provider.address.like("%"+address+"%")).all()

    elif stars and not name and not address:
        providers = Provider.query.filter(Provider.rating_avg >= stars).all()
    
    elif name and address and not stars:
        providers1 = Provider.query.filter(Provider.provider_name.like("%"+name+"%")).all()
        providers2 = Provider.query.filter(Provider.address.like("%"+address+"%")).all()
        providers = [provider for provider in providers1 if provider in providers2]

    elif name and stars and not address:
        providers1 = Provider.query.filter(Provider.provider_name.like("%"+name+"%")).all()
        providers2 = Provider.query.filter(Provider.rating_avg >= stars).all()
        providers = [provider for provider in providers1 if provider in providers2]

    elif stars and address and not name:
        providers1 = Provider.query.filter(Provider.address.like("%"+address+"%")).all()
        providers2 = Provider.query.filter(Provider.rating_avg >= stars).all()
        providers = [provider for provider in providers1 if provider in providers2]

    elif name and stars and address:
        providers1 = Provider.query.filter(Provider.provider_name.like("%"+name+"%")).all()
        providers2 = Provider.query.filter(Provider.address.like("%"+address+"%")).all()
        providers3 = Provider.query.filter(Provider.rating_avg >= stars).all()
        providers4 = [provider for provider in providers1 if provider in providers2]
        providers = [provider for provider in providers3 if provider in providers4]


    if service=='Appliances':
        result = Service.query.filter_by(category="Appliances").all()
    elif service=='Electrical':
        result = Service.query.filter_by(category="Electrical").all()
    elif service=='Plumbing':
        result = Service.query.filter_by(category="Plumbing").all()
    elif service=='Cleaning':
        result = Service.query.filter_by(category="Cleaning").all()
    elif service=='Tutoring':
        result = Service.query.filter_by(category="Tutoring").all()
    elif service=='Moving':
        result = Service.query.filter_by(category="Moving").all()
    elif service=='Computer':
        result = Service.query.filter_by(category="Computer").all()
    elif service=='Painting':
        result = Service.query.filter_by(category="Painting").all()
    elif service=='Pest Control':
        result = Service.query.filter_by(category="Pest Control").all()

    
    return render_template('services.html', result=result, providers = providers, service = service)
    
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