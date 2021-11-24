from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Service
from . import db

search = Blueprint('search', __name__)

@search.route('/search')
def searching():
    return render_template('search.html')

@search.route('/search', methods=['POST'])
def searching_post():
	searchInput = request.form.get('searchInput')
	results = Service.query.msearch(searchInput).all()
	return redirect(url_for('main.profile'))