


from flask import Blueprint, render_template, request
from . import db
from .models import Provider, Service
from flask_login import login_required, current_user

from sqlalchemy import *




providerController = Blueprint('providerController', __name__)




@providerController.route('/providers')
def providers():
    provider_id_from_client=request.args.get('provider_id')
    service_id_from_client = request.args.get('service_id')
    result = Provider.query.filter_by(provider_id=provider_id_from_client).all()
    service_result = Service.query.filter_by(service_id=service_id_from_client)
    return render_template('order.html',provider_id = provider_id_from_client, service_id = service_id_from_client, providers=result, services=service_result, user = current_user)