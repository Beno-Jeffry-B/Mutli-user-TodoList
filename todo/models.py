from todo import db


class User(db.Model):
    user_id = db.Column(db.Integer , primary_key = True)
    user_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(30))
    
    # Relationship: one user can have many tasks
    tasks = db.relationship('Tasks', backref='user', lazy=True)

class Tasks(db.Model):
    task_id = db.Column(db.Integer , primary_key = True)
    tasks = db.Column(db.String(100))
    status = db.Column(db.Boolean , default = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.user_id')) 
