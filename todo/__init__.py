from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "demo"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo_app_db.db"
db = SQLAlchemy(app)


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


from todo import models
from todo import routes

with app.app_context():
    db.create_all()


