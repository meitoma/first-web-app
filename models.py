from __init__ import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from zoneinfo import ZoneInfo

class Users(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(256))
    messages = db.relationship('Messages', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<Users {self.name}>'
            
    def set_password(self,password):
        self.password = generate_password_hash(password)
        print(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def add_user(self):
        self.set_password(self.password)
        db.session.add(self)
        db.session.commit()

class Messages(UserMixin,db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    message = db.Column(db.String(256))
    sendtime = db.Column(db.DateTime, default=datetime.datetime.now(ZoneInfo("Asia/Tokyo")))

    def __repr__(self):
        return f'<Messages {self.messages}>'
    
    def add_message(self):
        db.session.add(self)
        db.session.commit()
    
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))