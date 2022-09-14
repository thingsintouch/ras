from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# class OptionsForm(FlaskForm):
#     device_name = StringField('New Device Name', validators=[DataRequired(),
#                     Length(min=1, max=12, message="The Device Name should have a length between %(min)d and %(max)d")])
#     submit_device_name = SubmitField('Change Device Name')
