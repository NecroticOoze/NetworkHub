from flask_login import UserMixin
from app import db, login_manager
from datetime import datetime
import time

# t = time.localtime()
# current_time = time.strftime("%H:%M:%S", t)
# print(current_time)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), nullable=False, unique=True)
    password = db.Column(db.Unicode(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    role = db.Column(db.Unicode(255), nullable=False, default='user')

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Unicode(255), nullable=False)
    drive = db.Column(db.Unicode(255), nullable=False)
    filename = db.Column(db.Unicode(255), nullable=False)
    uuid_name = db.Column(db.Unicode(255), nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    date_uploaded = db.Column(db.Unicode(100), nullable=False, default=time.strftime("%D", time.localtime()))