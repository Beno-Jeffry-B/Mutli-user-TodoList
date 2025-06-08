from todo import db


class User(db.Model):
    user_id = db.Column(db.Integer , primary_key = True)
    user_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(30))
    
    # Relationship: one user can have many tasks
    tasks = db.relationship('Tasks', backref='user', lazy=True)

from datetime import datetime
from todo import db

class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    tasks = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(10), default='Low')
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='not_started')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))


