from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_mail import Mail
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TASKIFY.db'
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') #Sender Email
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')    # ender Email Password

mail = Mail(app)
mail.init_app(app)  # initialize mail with app




from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


from todo import models
from todo import routes

with app.app_context():
    db.create_all()


