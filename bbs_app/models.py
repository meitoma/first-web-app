from __init__ import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import datetime
from zoneinfo import ZoneInfo

class Users(UserMixin,db.Model):
    __tablename__ = 'users'
    admin=db.Column(db.Boolean, default=False)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(256))
    messages = db.relationship('Messages', backref=db.backref('users', lazy=True))
    user_access = db.relationship('UserAccess', backref=db.backref('users', lazy=True))
    fcm_token = db.relationship('FCMToken', backref=db.backref('users', lazy=True))
    ws_access = db.relationship('WSAccessUser', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<Users {self.name}>'
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_anonymous(self):
        return False
    
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
    thread_id = db.Column(db.Integer,db.ForeignKey('threads.id'))
    message_type=db.Column(db.String(10))
    message = db.Column(db.String(256))
    sendtime = db.Column(db.DateTime, default=datetime.datetime.now(ZoneInfo("Asia/Tokyo")))

    def __repr__(self):
        return f'<Messages {self.message}>'
    
    def add_message(self):
        db.session.add(self)
        db.session.commit()

class Threads(UserMixin,db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    thread_name = db.Column(db.String(256))
    ws_id = db.Column(db.Integer,db.ForeignKey('work_spaces.id'))
    messages = db.relationship('Messages', backref=db.backref('threads', lazy=True))
    user_access = db.relationship('UserAccess', backref=db.backref('threads', lazy=True))

    def __repr__(self):
        return f'<Threads {self.thread_name}>'

    def add_threads(self):
        db.session.add(self)
        db.session.commit()

class UserAccess(UserMixin,db.Model):
    __tablename__ = 'user_access'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    thread_id = db.Column(db.Integer,db.ForeignKey('threads.id'))

    def add_user_access(self):
        db.session.add(self)
        db.session.commit()

class WorkSpaces(UserMixin,db.Model):
    __tablename__ = 'work_spaces'
    id = db.Column(db.Integer, primary_key=True)
    ws_name = db.Column(db.String(256))
    ws_token = db.Column(db.String(256))
    update_time = db.Column(db.DateTime, default=datetime.datetime.now(ZoneInfo("Asia/Tokyo")))
    ws_access_user = db.relationship('WSAccessUser', backref=db.backref('work_spaces', lazy=True))
    threads = db.relationship('Threads', backref=db.backref('work_spaces', lazy=True))

    def add_threads(self):
        db.session.add(self)
        db.session.commit()

class WSAccessUser(UserMixin,db.Model):
    __tablename__ = 'ws_access_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    ws_id = db.Column(db.Integer,db.ForeignKey('work_spaces.id'))

    def add_user_access(self):
        db.session.add(self)
        db.session.commit()

class FCMToken(UserMixin,db.Model):
    __tablename__ = 'fcm_token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))