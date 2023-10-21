from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length
from common.common import pPrint

class CommandForm(FlaskForm):
    command_update = SubmitField('Update')
    command_reboot = SubmitField('Reboot')
    command_partial_reset = SubmitField('Partial Reset')
    command_full_reset = SubmitField('Full Reset')
    command_shutdown = SubmitField('Shutdown')
    command_delete_clockings = SubmitField('Delete clockings')
    command_set_ethernet_mac= SubmitField('Set Ethernet MAC')
    command_delete_IPs =  SubmitField('Delete all IP addresses')
    command_send_emailLogs = SubmitField('Send Email with Log of last 500 registered cards')
    command_marry_router = SubmitField('Associate current router permanently to the device')
    command_divorce_router = SubmitField('Remove any association to a specific router')

class CommandResult(FlaskForm):
    submit = SubmitField('OK')
    cancel = SubmitField('Cancel')
