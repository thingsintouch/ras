from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from common.params import Params
from common.constants import PARAMS
from factory_settings.custom_params import factory_settings 

params = Params(db=PARAMS)

factory = Blueprint('factory',__name__)

@factory.route('/factory',methods=['GET','POST'])
@login_required
def show_factory_settings():
    return render_template('factory.html',fs=factory_settings)
