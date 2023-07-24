from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from setup_server.commands.forms import CommandForm, CommandResult
from common.common import runShellCommand_and_returnOutput as rs
from common.common import pPrint
from common.params import Params
from common.constants import PARAMS
from odoo.routineCheck import saveChangesToParams

params = Params(db=PARAMS)

commands = Blueprint('commands',__name__)

commands_list = [
    ('0', 'command_update', 'Update the Firmware', "shouldGetFirmwareUpdate"),
    ('1', 'command_reboot', 'Reboot the Device', "rebootTerminal"),
    ('2', 'command_partial_reset', 'Partial Reset', "partialFactoryReset"),
    ('3', 'command_full_reset', 'Full Factory Reset', "fullFactoryReset"),
    ('4', 'command_shutdown', 'Shutdown the Device', "shutdownTerminal"),
    ('5', 'command_delete_clockings', 'Delete clockings stored in the device', "deleteClockings"),
    ('6', 'command_set_ethernet_mac', 'Set the Ethernet Mac to match the MAC of the Raspberry Pi', "setEthernetMAC"),
    ]
# options_list = [
#     ('0', 'option_device_name', 'device_name', "RASxxx", "The device name "),
#     ('1', 'option_time_format', 'time_format', "time_format", "The time format "),
#     ('2', 'option_tz', 'tz', "tz", "The time zone "),
#     ('3', 'option_text_card', 'text_card', "card_registered", "The text to be displayed when a card is swiped "),
#     ('4', 'option_min_time', 'min_time', "minimumTimeBetweenClockings", "The minimum time (in seconds) to wait between clockings "),
#     ('5', 'option_text_too_soon', 'text_too_soon', "too_little_time_between_clockings", "The text to be displayed when a card is swiped too soon "),
#     ('6', 'option_period_register_clockings', 'period_register_clockings', "period_register_clockings", "The terminal will send new clockings to Odoo in a period in seconds "),
#     ('7', 'option_setup_password', 'setup_password', "setup_password", "The password "),
#     ('8', 'option_display_time', 'display_time', "timeToDisplayResultAfterClocking", "The display time (in seconds) "),
#     ('9', 'option_odooUrlTemplate', 'odooUrlTemplate', "odooUrlTemplate", "The URL template to communicate with Odoo "),
#     ('10', 'option_odoo_host', 'odoo_host', "odoo_host", "The Odoo server host "),
#     ('11', 'option_odoo_port', 'odoo_port', "odoo_port", "The Odoo server port "),
#     ('12', 'option_register_template', 'register_template', "template_to_register_device", "The template used to register the device in Odoo "),
#     ('13', 'option_runs_locally', 'runs_locally', "RAS_runs_locally", "The parameter to indicate if the device runs locally "),
#     ('14', 'option_clockings_expiration', 'clockings_expiration', "clockings_expiration_period_in_weeks", "The clockings expiration period (how many weeks after which the clockings will be deleted from local storage) "),  
#      ]

@commands.route('/commands',methods=['GET','POST'])
@login_required
def take_command():
    form = CommandForm()
    # if request.method == 'GET':
    #     form.device_name.data = params.get("RASxxx") or "Entrance"
    #     form.time_format.data = params.get("time_format") or "24 hour"
    #     form.tz.data = params.get("tz") or "Europe/Berlin"
    #     form.text_card.data = params.get("card_registered") or "Hello"
    #     form.min_time.data = params.get("minimumTimeBetweenClockings") or "300"
    #     form.text_too_soon.data = params.get("too_little_time_between_clockings") or "Too soon"
    #     form.period_register_clockings.data = params.get("period_register_clockings") or "60"
    #     form.setup_password.data = params.get("setup_password") or "password not set"
    #     form.display_time.data = params.get("timeToDisplayResultAfterClocking") or "time not set"
    #     form.odooUrlTemplate.data = params.get("odooUrlTemplate") or "not set"
    #     form.odoo_host.data = params.get("odoo_host") or "not set"
    #     form.odoo_port.data = params.get("odoo_port") or "not set"
    #     form.register_template.data = params.get("template_to_register_device") or "not set"
    #     form.runs_locally.data = params.get("RAS_runs_locally") or "0"
    #     form.clockings_expiration.data = params.get("clockings_expiration_period_in_weeks") or "2"
    if form.is_submitted():
        for c in commands_list:
            if c[1] in request.form:
                command = c[0]
                return redirect(url_for('commands.command_result', command=command ))
        # for o in options_list:
        #     if o[1] in request.form:
        #         #pPrint(list(request.form.keys()))
        #         #pPrint(o[3])
        #         #pPrint(request.form[o[2]])
        #         saveChangesToParams({o[3]:request.form[o[2]]})
        #         option = o[0]
        #         return redirect(url_for('commands.option_result', option=option ))
    return render_template('commands.html', form=form)

@commands.route('/commands/<int:command>',methods=['GET','POST'])
@login_required
def command_result(command):
    command_text = commands_list[command][2]
    form=CommandResult()
    if form.validate_on_submit():
        if form.cancel.data:
            pass
        else:
            booleanFlag = commands_list[command][3]
            params.put(booleanFlag,"1")
        return redirect(url_for('commands.take_command'))

    return render_template('command_result.html', form=form, command=command_text)

# @commands.route('/options/<int:option>',methods=['GET','POST'])
# @login_required
# def option_result(option):
#     option_text = options_list[option][4]
#     value = params.get(options_list[option][3])
#     form=CommandResult()
#     if form.validate_on_submit():
#         return redirect(url_for('commands.take_command'))

#     return render_template('option_result.html', form=form, option=option_text, value=value)
