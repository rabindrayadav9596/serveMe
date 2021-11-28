from flask import Blueprint, render_template, request,redirect, url_for
from .models import User
from . import db
from flask_login import login_required, current_user

setting = Blueprint('setting', __name__)

@setting.route('/settings', methods=["POST"])
def settings_save():
    checkState1=request.form.get("checkState1")
    checkState2=request.form.get("checkState2")
    checkState3=request.form.get("checkState3")
    checkState4=request.form.get("checkState4")
    settings=""
    if checkState1:
        settings+='1'
    else:
        settings+='0'
    if checkState2:
        settings+='1'
    else:
        settings+='0'
    if checkState3:
        settings+='1'
    else:
        settings+='0'
    if checkState4:
        settings+='1'
    else:
        settings+='0'
    current_user.settings= settings
    db.session.commit()
    return redirect(url_for("setting.settings_retrieve"))	


@setting.route('/settings', methods=['GET'])
def settings_retrieve():
    user=current_user;
    settings = list(user.settings)
    checkState1=settings[0]
    checkState2=settings[1]
    checkState3=settings[2]
    checkState4=settings[3]
    if checkState1=='0':
        checkState1Str="unchecked"
    else:
        checkState1Str="checked"
    
    if checkState2=='0':
        checkState2Str="unchecked"
    else:
        checkState2Str="checked"
    
    if checkState3=='0':
        checkState3Str="unchecked"
    else:
        checkState3Str="checked"
    
    if checkState4=='0':
        checkState4Str="unchecked"
    else:
        checkState4Str="checked"    

    return render_template('settings.html', checkState1=checkState1Str, checkState2=checkState2Str, checkState3=checkState3Str,checkState4=checkState4Str)


    