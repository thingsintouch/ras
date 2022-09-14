from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length
from common.common import pPrint
from odoo.routineCheck import tz_list

time_format_choices = [("12 hour", "12 hour"), ("24 hour", "24 hour")]
tz_choices =[]
for t in tz_list:
    tz_choices.append((t,t))

class ParametersForm(FlaskForm):
    clockings_expiration = IntegerField('How long (in weeks) to keep clockings not recorded on Odoo but stored in device before deleting (2 to 12 weeks)')
    option_clockings_expiration = SubmitField('Change expiration limit')
    
    odooUrlTemplate = StringField('Odoo-URL template')
    option_odooUrlTemplate = SubmitField('Change URL')

    odoo_host = StringField('Odoo server host')
    option_odoo_host = SubmitField('Change host') 

    odoo_port = StringField('Odoo server port')
    option_odoo_port = SubmitField('Change port')

    register_template = StringField('Template used to register the device in Odoo')
    option_register_template = SubmitField('Change register template')

    runs_locally = SelectField(u'RAS runs on localnet (no internet)',
        choices=[("0","connected to internet"), ("1","only connected to local net")])
    option_runs_locally = SubmitField('Set')

    display_time = StringField('How long to show the message on the display after swiping a card (1.0-4.0 seconds)')
    option_display_time = SubmitField('Change display time')     

    setup_password = StringField('Password for this server')
    option_setup_password = SubmitField('Change password') 

    device_name = StringField('Device name')
    option_device_name = SubmitField('Change device name')

    time_format = SelectField(u'Select a time format',
        choices=time_format_choices)
    option_time_format = SubmitField('Set time format')

    tz = SelectField(u'Select a time zone',
        choices=tz_choices)
    option_tz = SubmitField('Set time zone')

    text_card = StringField('New text to be displayed when a card is swiped ')
    option_text_card = SubmitField('Change display text')

    min_time = IntegerField('Minimum time to wait between clockings (0-30000 seconds)')
    option_min_time = SubmitField('Change the minimum time')

    text_too_soon = StringField('Text to be displayed when a card is swiped too soon')
    option_text_too_soon = SubmitField('Change -too soon- text')

    period_register_clockings = IntegerField('The terminal will send new clockings to Odoo in a period of (14-3600 seconds)')
    option_period_register_clockings = SubmitField('Change the period')

    # command_update = SubmitField('Update')
    # command_reboot = SubmitField('Reboot')
    # command_partial_reset = SubmitField('Partial Reset')
    # command_full_reset = SubmitField('Full Reset')
    # command_shutdown = SubmitField('Shutdown')
    # command_delete_clockings = SubmitField('Delete clockings')


class ParametersResult(FlaskForm):
    submit = SubmitField('OK')
    cancel = SubmitField('Cancel')