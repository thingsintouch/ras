from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from setup_server.parameters.forms import ParametersForm, ParametersResult
from common.common import runShellCommand_and_returnOutput as rs
from common.common import pPrint
from common.params import Params
from common.constants import PARAMS
from odoo.routineCheck import saveChangesToParams

params = Params(db=PARAMS)

parameters = Blueprint('parameters',__name__)

options_list = [
    ('0', 'option_device_name', 'device_name', "RASxxx", "The device name "),
    ('1', 'option_time_format', 'time_format', "time_format", "The time format "),
    ('2', 'option_tz', 'tz', "tz", "The time zone "),
    ('3', 'option_text_card', 'text_card', "card_registered", "The text to be displayed when a card is swiped "),
    ('4', 'option_min_time', 'min_time', "minimumTimeBetweenClockings", "The minimum time (in seconds) to wait between clockings "),
    ('5', 'option_text_too_soon', 'text_too_soon', "too_little_time_between_clockings", "The text to be displayed when a card is swiped too soon "),
    ('6', 'option_period_register_clockings', 'period_register_clockings', "period_register_clockings", "The terminal will send new clockings to Odoo in a period in seconds "),
    ('7', 'option_setup_password', 'setup_password', "setup_password", "The password "),
    ('8', 'option_display_time', 'display_time', "timeToDisplayResultAfterClocking", "The display time (in seconds) "),
    ('9', 'option_odooUrlTemplate', 'odooUrlTemplate', "odooUrlTemplate", "The URL template to communicate with Odoo "),
    ('10', 'option_odoo_host', 'odoo_host', "odoo_host", "The Odoo server host "),
    ('11', 'option_odoo_port', 'odoo_port', "odoo_port", "The Odoo server port "),
    ('12', 'option_register_template', 'register_template', "template_to_register_device", "The template used to register the device in Odoo "),
    ('13', 'option_runs_locally', 'runs_locally', "RAS_runs_locally", "The parameter to indicate if the device runs locally "),
    ('14', 'option_clockings_expiration', 'clockings_expiration', "clockings_expiration_period_in_weeks", "The clockings expiration period (how many weeks after which the clockings will be deleted from local storage) "),
    ('15', 'option_show_in_out', 'show_in_out', "show_checkin_or_out_display", "Should the terminal show an estimation if the clocking is checkin or checkout"),
    ('16', 'option_check_in_message_display', 'check_in_message_display', "check_in_message_display", "The message to be shown on the display for a CHECK-IN"),
    ('17', 'option_check_out_message_display', 'check_out_message_display', "check_out_message_display", "The message to be shown on the display for a CHECK-OUT"),
    ('18', 'option_show_debug', 'show_debug', "show_debug", "Should the terminal log DEBUG messages"),
    ]

@parameters.route('/parameters',methods=['GET','POST'])
@login_required
def take_parameter():
    form = ParametersForm()
    if request.method == 'GET':
        form.device_name.data = params.get("RASxxx") or "Entrance"
        form.time_format.data = params.get("time_format") or "24 hour"
        form.tz.data = params.get("tz") or "Europe/Berlin"
        form.text_card.data = params.get("card_registered") or "Hello"
        form.min_time.data = params.get("minimumTimeBetweenClockings") or "300"
        form.text_too_soon.data = params.get("too_little_time_between_clockings") or "Too soon"
        form.period_register_clockings.data = params.get("period_register_clockings") or "60"
        form.setup_password.data = params.get("setup_password") or "password not set"
        form.display_time.data = params.get("timeToDisplayResultAfterClocking") or "time not set"
        form.odooUrlTemplate.data = params.get("odooUrlTemplate") or "not set"
        form.odoo_host.data = params.get("odoo_host") or "not set"
        form.odoo_port.data = params.get("odoo_port") or "not set"
        form.register_template.data = params.get("template_to_register_device") or "not set"
        form.runs_locally.data = params.get("RAS_runs_locally") or "0"
        form.clockings_expiration.data = params.get("clockings_expiration_period_in_weeks") or "2"
        form.show_in_out.data = params.get("show_checkin_or_out_display") or "0"
        form.check_in_message_display.data = params.get("check_in_message_display") or "CHECK IN"
        form.check_out_message_display.data = params.get("check_out_message_display") or "CHECK OUT"
        form.show_debug.data = params.get("show_debug") or "0"
    if form.is_submitted():
        for o in options_list:
            if o[1] in request.form:
                #pPrint(list(request.form.keys()))
                #pPrint(o[3])
                #pPrint(request.form[o[2]])
                saveChangesToParams({o[3]:request.form[o[2]]})
                option = o[0]
                return redirect(url_for('parameters.option_result', option=option ))
    return render_template('parameters.html', form=form)


@parameters.route('/options/<int:option>',methods=['GET','POST'])
@login_required
def option_result(option):
    option_text = options_list[option][4]
    value = params.get(options_list[option][3])
    form=ParametersResult()
    if form.validate_on_submit():
        return redirect(url_for('parameters.take_parameter'))

    return render_template('option_result.html', form=form, option=option_text, value=value)
