

from flask import Blueprint, render_template, request
from . import db
from .models import Service

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
    return render_template('services.html', result=result, serv = service)