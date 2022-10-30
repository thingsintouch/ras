from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from setup_server.wifi_setup.forms import WiFiForm, WiFiSetupResult
from common.common import runShellCommand_and_returnOutput as rs
from common.connect_To_SSID import store_wifi_network_and_password #main as connect_to_wifi_network
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
        if store_wifi_network_and_password(wifi_network, wifi_password):
            result = 1 
        else:
            result = 0
        return redirect(url_for('wifi_setup.wifi_setup_result', result=result ))
    return render_template('wifi_setup.html', form=form)

@wifi_setup.route('/wifi_setup/<int:result>',methods=['GET','POST'])
@login_required
def wifi_setup_result(result):
    form=WiFiSetupResult()
    if result == 1:
        result_for_html = "Connected successfully."
    else:
        result_for_html = "Failed. Could not connect to WiFi network."

    if form.validate_on_submit():
        return redirect(url_for('odoo_setup.odoo_link'))

    return render_template('wifi_setup_result.html', result=result_for_html, form=form)
    