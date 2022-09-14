from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
from common.common import pPrint


class OdooForm(FlaskForm):
    odoo_link = StringField('Odoo Link', validators=[DataRequired()])
    submit = SubmitField('Connect')

class OdooResult(FlaskForm):
    submit = SubmitField('OK')