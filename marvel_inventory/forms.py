from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit_button = SubmitField()