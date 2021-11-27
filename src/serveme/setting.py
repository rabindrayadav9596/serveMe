
from flask import Blueprint, render_template


setting = Blueprint('setting', __name__)


@setting.route('/settings')

def settings():
    return render_template('settings.html')
    