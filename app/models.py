from flask_login import UserMixin
from app import db, login_manager,app
from datetime import datetime
import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

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

    def get_valid_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_valid_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Unicode(255), nullable=False)
    drive = db.Column(db.Unicode(255), nullable=False)
    filename = db.Column(db.Unicode(255), nullable=False)
    uuid_name = db.Column(db.Unicode(255), nullable=False)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    date_uploaded = db.Column(db.Unicode(100), nullable=False, default=time.strftime("%D", time.localtime()))