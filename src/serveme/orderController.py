from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Service, Provider, Order
from flask_login import login_required, current_user
from sqlalchemy import *
import datetime
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta


orderController = Blueprint('orderController', __name__)





@orderController.route('/order', methods=['POST'])
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
        return redirect(url_for('providerController.providers', provider_id = provider_id, service_id = service_id, providers=result, services=service_result))
    elif date > future_date:
        flash("You cannot schedule services in more than one year, try again!")
        return redirect(url_for('providerController.providers', provider_id = provider_id, service_id = service_id, providers=result, services=service_result))
    else:
        provider_id=request.args.get('provider_id')
        service_id = request.args.get('service_id')
        cost = request.args.get('cost')
        description = request.args.get('description')
        new_order = Order(provider_id=provider_id,service_id=service_id, userID=current_user.userID, cost=cost,  description=description, date=date, status = "InProgress")
        db.session.add(new_order)
        db.session.commit()
        return render_template('order_confirmation.html')
    

@orderController.route('/past_orders')
def past_orders():
    currentDate = datetime.now()
    orders = Order.query.filter(or_(Order.status == 'Completed', Order.status == "Canceled"), Order.userID==current_user.userID).all()    
    services = Service.query.all()
    providers = Provider.query.all()
    return render_template('past_orders.html', orders=orders, services=services, providers=providers)  

@orderController.route('/current_orders')
def current_orders():
    currentDate = datetime.now()
    orders = Order.query.filter(or_(Order.status == 'InProgress', Order.status == "Accepted"), Order.userID==current_user.userID).all()    
    services = Service.query.all()
    providers = Provider.query.all()
    return render_template('current_orders.html', orders=orders, services=services, providers=providers)  

@orderController.route('/current_orders', methods=['POST'])
def cancel_current_order():
    orderID=request.args.get('orderID')
    if request.form.get('modifyDate') == 'modifyDate':
       return redirect(url_for('orderController.modify_date', orderID=orderID))
    elif request.form.get('cancelOrder') == "cancelOrder":
        order = Order.query.filter_by(order_id=orderID).first()
        order.status = "Canceled"
        db.session.commit()
        return redirect(url_for('orderController.current_orders'))

@orderController.route('/modify_date')
def modify_date():
    orderID = request.args.get('orderID')
    return render_template('modify_date.html', orderID=orderID)  

@orderController.route('/modify_date', methods=['POST'])
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
        return redirect(url_for('orderController.modify_date_post', orderID=orderID))
    elif date > future_date:
        flash("You cannot schedule services in more than one year, try again!")
        return redirect(url_for('orderController.modify_date_post',orderID=orderID))
    else:
        order = Order.query.filter_by(order_id=orderID).first()
        order.date = date
        db.session.commit()
    return redirect(url_for('orderController.current_orders'))



@orderController.route('/requested_orders_provider')
@login_required
def requested_orders_provider():
    # users = Users.query.filter()
    # provider_id = Provider.query.filter(Provider.userID == current_user.userID).first()
    # orders = Order.query.filter( Order.provider_id==provider_id).all()    
    # services = Service.query.all()
    provider = Provider.query.filter_by(userID = current_user.userID).first()
    provider_id = provider.provider_id
    orders = Order.query.filter_by(provider_id = provider_id).all()
    services = Service.query.filter_by(provider_id = provider_id )
    return render_template('requested_orders_provider.html', provider = provider, user=current_user, orders = orders, services = services)




@orderController.route('/requested_orders_provider', methods=['POST'])
@login_required
def change_service_status():
    orderID=request.args.get('orderID')
    if request.form.get('acceptOrder') == 'acceptOrder':
        order = Order.query.filter_by(order_id=orderID).first()
        order.status = "Accepted"
        db.session.commit()
    elif request.form.get('cancelOrder') == "cancelOrder":
        order = Order.query.filter_by(order_id=orderID).first()
        order.status = "Canceled"
        db.session.commit()
    elif request.form.get('completeOrder') == "completeOrder":
        order = Order.query.filter_by(order_id=orderID).first()
        order.status = "Completed"
        db.session.commit()
 
    provider = Provider.query.filter_by(userID = current_user.userID).first()
    provider_id = provider.provider_id
    orders = Order.query.filter_by(provider_id = provider_id).all()
    services = Service.query.filter_by(provider_id = provider_id )
    return redirect(url_for('orderController.requested_orders_provider',provider = provider, user=current_user, orders = orders, services = services))


   
@orderController.route('/past_orders_provider')
@login_required
def past_orders_provider():
    provider = Provider.query.filter_by(userID = current_user.userID).first()
    provider_id = provider.provider_id
    orders = Order.query.filter_by(provider_id = provider_id).all()
    services = Service.query.filter_by(provider_id = provider_id )
    return render_template('past_orders_provider.html', provider = provider, user=current_user, orders = orders, services = services)




