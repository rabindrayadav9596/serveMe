from flask import Blueprint, render_template, request
from . import db
from .models import Provider, Service
from sqlalchemy import *
from flask_login import login_required, current_user

providerController = Blueprint('providerController', __name__)

@providerController.route('/providers')
def providers():
    provider_id_from_client=request.args.get('provider_id')
    service_id_from_client = request.args.get('service_id')
    points = round(current_user.points,2)
    result = Provider.query.filter_by(provider_id=provider_id_from_client).all()
    service_result = Service.query.filter_by(service_id=service_id_from_client)
    cost= service_result[0].cost
    total_cost=round(0.08*cost+cost,2)
    discounted=total_cost
    if total_cost>points:
        discounted=round(total_cost-points,2)
    else:
    	discounted=0
    return render_template('order.html',provider_id = provider_id_from_client, service_id = service_id_from_client, providers=result, services=service_result,cost=cost,totalcost=total_cost,discounted=discounted, points=points)