
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField


class login(FlaskForm):
    user_name = StringField(label='user_name')
    password = PasswordField(label='password')

class sign_up(FlaskForm):
    user_name = StringField(label='user_name')
    email = EmailField(label='email')
    password = PasswordField(label='password')
    confirm_password = PasswordField(label="confirm_password")
    
