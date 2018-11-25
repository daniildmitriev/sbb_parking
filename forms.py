from flask_wtf import FlaskForm
from wtforms import  BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired



class SignupForm(FlaskForm):
    name = StringField(u'Your name', validators=[DataRequired()])
    submit = SubmitField(u'Signup')

class DashboardReserveForm(FlaskForm):
    status_button = SubmitField(u'Reserve')

class DashboardConfirmForm(FlaskForm):
    status_button = SubmitField(u'Confirm')

class DashboardLogoutForm(FlaskForm):
    status_button = SubmitField(u'Logout')