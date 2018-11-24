from flask_wtf import FlaskForm
from wtforms import  BooleanField, StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired


class SignupForm(FlaskForm):
    name = StringField(u'Your name', validators=[DataRequired()])

    submit = SubmitField(u'Signup')
