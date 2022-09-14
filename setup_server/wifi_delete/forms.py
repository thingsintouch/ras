from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
from common.common import runShellCommand_and_returnOutput as rs
from common.common import pPrint

def get_existent_connections():
    answer = (rs("nmcli --terse connection show"))
    if answer and answer is not None:
        existent_connections = answer.split('\n')
    wifi_connections = []
    for c in existent_connections:
        if "wireless" in c:
            c_splitted = c.split(":")
            wifi_connections.append((c_splitted[1], c_splitted[0])) # 0 is SSID name, 1 is UUID for nmcli
    pPrint(wifi_connections)
    return  wifi_connections


class WiFiDelete(FlaskForm):

    # refresh_list = BooleanField('Refresh list')
    existent_connections = get_existent_connections()
    connection_to_delete = SelectField(u'Select a connection to delete:',
        choices=existent_connections, validators=[DataRequired()])
    submit = SubmitField('Delete')

class WiFiDeleteResult(FlaskForm):
    submit = SubmitField('OK')