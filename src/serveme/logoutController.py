from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Provider
from . import db
import uuid

logoutController = Blueprint('logoutController', __name__)

@logoutController.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))