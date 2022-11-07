from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from setup_server.wifi_setup.forms import WiFiForm, WiFiSetupResult
from common.common import runShellCommand_and_returnOutput as rs
from common.common import store_wifi, get_wifi, connect_to_wifi_through_d_bus_method 
from common.counter_ops import reset_counter

wifi_setup = Blueprint('wifi_setup',__name__)

@wifi_setup.route('/wifi_setup',methods=['GET','POST'])
@login_required
def define_wifi():
    form = WiFiForm()
    if form.validate_on_submit():
        #reset_counter("counter_wifi_disconnected")
        wifi_network = form.wifi_network.data
        wifi_password = form.password.data

        store_wifi(wifi_network, wifi_password)
        
        return redirect(url_for('wifi_setup.wifi_confirm_page'))
    return render_template('wifi_setup.html', form=form)

@wifi_setup.route('/wifi_confirm_page>',methods=['GET','POST'])
@login_required
def wifi_connect_confirm_page(result):
    wifi_network, wifi_password = get_wifi()
    form = WiFiSetupResult()
    if form.validate_on_submit():
        connect_to_wifi_through_d_bus_method()
        return redirect(url_for('odoo_setup.odoo_link'))

    return render_template('wifi_setup_result.html', wifi_network=wifi_network, wifi_password=wifi_password, form=form)
    