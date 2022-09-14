from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
from common.connectivity import get_available_networks

class WiFiForm(FlaskForm):
    available_networks = get_available_networks()
    wifi_network = SelectField(u'Select a WiFi network:',
        choices=available_networks, validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Connect')

class WiFiSetupResult(FlaskForm):
    submit = SubmitField('OK')