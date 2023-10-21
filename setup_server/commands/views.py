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
    ('6', 'command_set_ethernet_mac', 'Set the Ethernet MAC Address of the Device to match the MAC Address of the Raspberry Pi and not the MAC Address of the Adapter', "setEthernetMAC"),
    ('7', 'command_delete_IPs', 'Delete the stored IP Addresses for Ethernet and WiFi', "deleteIPs"),
    ('8', 'command_send_emailLogs', 'Send Email with Log of last 400 registered cards (define the Email before)', "send_emailLogs"),
    ('9', 'command_marry_router', 'Associate current router permanently to the device', "marry_router"),
    ('10', 'command_divorce_router', 'Remove any association to a specific router', "divorce_router"),
    ]


@commands.route('/commands',methods=['GET','POST'])
@login_required
def take_command():
    form = CommandForm()

    if form.is_submitted():
        for c in commands_list:
            if c[1] in request.form:
                command = c[0]
                return redirect(url_for('commands.command_result', command=command ))
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
