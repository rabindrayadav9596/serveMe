

from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Service, Provider, Order
from flask_login import login_required, current_user
from datetime import datetime


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/services')
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
        result = Service.query.filter_by(category="HomeCleaning").all()
    elif service=='tutoring':
        result = Service.query.filter_by(category="Tutoring").all()
    elif service=='moving':
        result = Service.query.filter_by(category="Moving").all()
    elif service=='computer':
        result = Service.query.filter_by(category="Computer Repair").all()
    elif service=='painting':
        result = Service.query.filter_by(category="Painting").all()
    elif service=='pest_control':
        result = Service.query.filter_by(category="Pest Control").all()
    return render_template('services.html', result=result)

@main.route('/providers')
def providers():
    provider_id_from_client=request.args.get('provider_id')
    service_id_from_client = request.args.get('service_id')
    result = Provider.query.filter_by(provider_id=provider_id_from_client).all()
    service_result = Service.query.filter_by(service_id=service_id_from_client)
    return render_template('order.html', providers=result, services=service_result)


@main.route('/payment')
def payment():
    return render_template('payment.html')

@main.route('/order', methods=['POST'])
def order():
    date = request.form.get('date')
    time=request.form.get('time')
    date_time_str = date + ' ' + time
    date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    # date=datetime()
    provider_id=request.args.get('provider_id')
    service_id = request.args.get('service_id')
    cost = request.args.get('cost')
    description = request.args.get('description')
    new_order = Order(provider_id=provider_id,service_id=service_id, userID=current_user.userID, cost=cost,  description=description, date=date)
    db.session.add(new_order)
    db.session.commit()
    
    print(date)
    return render_template('order_confirmation.html')

@main.route('/order_history')
def order_history():
    
    orders = Order.query.all()
    services = Service.query.all()
    return render_template('order_history.html', orders=orders, services=services)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
