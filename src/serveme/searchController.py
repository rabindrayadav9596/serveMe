from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Service,Provider
from . import db

searchController = Blueprint('searchController', __name__)



@searchController.route('/search', methods=['POST'])
def searching_post():
	name = request.form.get('name')
	address = request.form.get('address')
	stars = request.form.get('stars')
	service = request.args.get('service')
	# result = "none"
	
	# if service == 'Appliances':
    # 		result = Service.query.filter_by(category="Appliances").all()
	# elif service=="Electrical":
    # 		result = Service.query.filter_by(category="Electrical").all()
	# elif service == "Plumbing":
    # 		result = Service.query.filter_by(category="Plumbing").all()
	# elif service == "Cleaning":
    # 		result = Service.query.filter_by(category="Cleaning").all()
	# elif service == "Tutoring":
    # 		result = Service.query.filter_by(category="Tutoring").all()
	# elif service == "Moving":
    # 		result = Service.query.filter_by(category="Moving").all()
	# elif service == "Computer":
    # 		result = Service.query.filter_by(category="Computer").all()
	# elif service == "Painting":
    # 		result = Service.query.filter_by(category="Painting").all()
	# elif service == "Pest Control":
    # 		result = Service.query.filter_by(category="Pest Control").all()

	# providers = Provider.query.all()
	
	return redirect(url_for('serviceController.services', name = name, address = address, stars = stars, service = service))
