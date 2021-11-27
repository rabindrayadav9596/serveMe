
from flask import Blueprint, render_template


paymentController = Blueprint('paymentController', __name__)

@paymentController.route('/payment')
def payment():
    return render_template('payment.html')