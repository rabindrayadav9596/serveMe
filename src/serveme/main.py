from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Service, Provider, Order
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
    serviceice_id_from_client = request.args.get('service_id')
    result = Provider.query.filter_by(provider_id=provider_id_from_client).all()
    service_result = Service.query.filter_by(service_id=service_id_from_client)
    return render_template('order.html',provider_id = provider_id_from_client, service_id = service_id_from_client, providers=result, services=service_result)


@main.route('/payment')
def payment():
    return render_template('payment.html')

@main.route('/order', methods=['POST'])
def order():
    provider_id = request.args.get("provider_id")
    service_id = request.args.get("service_id")
    my_tz = pytz.timezone('America/Chicago')
    date = request.form.get('date')
    time=request.form.get('time')
    date_time_str = date + ' ' + time
    date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    date = my_tz.localize(date)

    my_datetime = datetime.now()   
    current_dt = my_tz.localize(my_datetime)
    future_date = current_dt + relativedelta(years=1)

    result = Provider.query.filter_by(provider_id=provider_id).all()
    service_result = Service.query.filter_by(service_id=service_id).all()

    if date < current_dt:
        flash("You cannot schedule services for the past, try again!")
        return redirect(url_for('main.providers', provider_id = provider_id, service_id = service_id, providers=result, services=service_result))
    elif date > future_date:
        flash("You cannot schedule services in more than one year, try again!")
        return redirect(url_for('main.providers', provider_id = provider_id, service_id = service_id, providers=result, services=service_result))
    else:
        provider_id=request.args.get('provider_id')
        service_id = request.args.get('service_id')
        cost = request.args.get('cost')
        description = request.args.get('description')
        new_order = Order(provider_id=provider_id,service_id=service_id, userID=current_user.userID, cost=cost,  description=description, date=date, status = "InProgress")
        db.session.add(new_order)
        db.session.commit()
        return render_template('order_confirmation.html')
    return render_template('profile.html')

@main.route('/past_orders')
def past_orders():
    currentDate = datetime.now()
    orders = Order.query.filter(Order.status=="Completed", Order.userID==current_user.userID).all()    
    services = Service.query.all()
    providers = Provider.query.all()
    return render_template('past_orders.html', orders=orders, services=services, providers=providers)  

@main.route('/current_orders')
def current_orders():
    currentDate = datetime.now()
    orders = Order.query.filter(Order.status=="InProgress", Order.userID==current_user.userID).all()    
    services = Service.query.all()
    providers = Provider.query.all()
    return render_template('current_orders.html', orders=orders, services=services, providers=providers)  

@main.route('/current_orders', methods=['POST'])
def cancel_current_order():
    orderID=request.args.get('orderID')
    if request.form.get('modifyDate') == 'modifyDate':
       return redirect(url_for('main.modify_date', orderID=orderID))
    elif request.form.get('cancelOrder') == "cancelOrder":
        order = Order.query.filter_by(order_id=orderID).first()
        order.status = "Canceled"
        db.session.commit()
        return redirect(url_for('main.current_orders'))

@main.route('/modify_date')
def modify_date():
    orderID = request.args.get('orderID')
    return render_template('modify_date.html', orderID=orderID)  

@main.route('/modify_date', methods=['POST'])
def modify_date_post():
    my_tz = pytz.timezone('America/Chicago')

    orderID = request.args.get('orderID')
    date = request.form.get('date')
    time=request.form.get('time')
    date_time_str = date + ' ' + time
    date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    date = my_tz.localize(date)

    my_datetime = datetime.now()   
    current_dt = my_tz.localize(my_datetime)
    future_date = current_dt + relativedelta(years=1)

    if date < current_dt:
        flash("You cannot schedule services for the past, try again!")
        return redirect(url_for('main.modify_date_post', orderID=orderID))
    elif date > future_date:
        flash("You cannot schedule services in more than one year, try again!")
        return redirect(url_for('main.modify_date_post',orderID=orderID))
    else:
        order = Order.query.filter_by(order_id=orderID).first()
        order.date = date
        db.session.commit()
    return redirect(url_for('main.current_orders'))


@main.route('/settings')
def settings():
    return render_template('settings.html')
    

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
