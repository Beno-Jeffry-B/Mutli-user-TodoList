
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,SubmitField
from wtforms.validators import EqualTo,Email,Length

class login(FlaskForm):
    user_name = StringField(label='user_name',
                            validators=[Length(max=50,min = 3)])  
     
    password = PasswordField(label='password',
                             validators=[Length(max=30 , min = 8)])

    submit = SubmitField(label='Login')
    
class sign_up(FlaskForm):
    user_name = StringField(label='user_name',
                            validators=[Length(max=50,min = 3)])
    
    email = EmailField(label='email',
                       validators=[Email() , Length(max=50)])
    
    password = PasswordField(label='password',
                             validators=[Length(max=30 , min = 8)])
    
    confirm_password = PasswordField(label="confirm_password" , 
                                     validators=[EqualTo('password',message=('Password must match with Confirm Password'))])
    submit = SubmitField(label='Sign up')



    
