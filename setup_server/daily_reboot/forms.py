from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from common.common import pPrint


class DailyRebootForm(FlaskForm):
    hour_reboot = IntegerField('Hour (0-23)',
        validators=[DataRequired(), 
            NumberRange(min=0, max=23, message="it has to be an integer between 0 and 23")])
    minute_reboot = IntegerField('Minute (0-59)',
        validators=[DataRequired(), 
            NumberRange(min=0, max=59, message="it has to be an integer between 0 and 59")])
    should_update_firmware_too = BooleanField('Update Firmware before rebooting?  ')

    submit = SubmitField('Submit new choices')

class DailyRebootResult(FlaskForm):
    submit = SubmitField('OK')