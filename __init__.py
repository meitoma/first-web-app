from flask import Flask,jsonify
import flask_login as login

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
import flask_login
from flask_wtf.csrf import CSRFProtect
from config import Config
import sys
import os
import firebase_admin
from firebase_admin import credentials, messaging

app = Flask(__name__,static_folder='bbs', template_folder='bbs/templates')
app.config.from_object(Config)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
metadata = MetaData()
socketio = SocketIO(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import Users,Messages,Threads,UserAccess,FCMToken
admin = Admin(
    app,
    name='Flask-admin laboratory',
    template_mode='bootstrap4',
)

class MyModelView1(sqla.ModelView):
    can_view_details = True
    def is_accessible(self):
        return not login.current_user.is_anonymous and login.current_user.is_admin

class MyModelView2(sqla.ModelView):
    can_view_details = True
    column_list = ["message","sendtime","user_id","thread_id"]
    column_sortable_list = column_list
    def is_accessible(self):
        return not login.current_user.is_anonymous and login.current_user.is_admin
    
class MyModelView3(sqla.ModelView):
    can_view_details = True
    def is_accessible(self):
        return not login.current_user.is_anonymous and login.current_user.is_admin

class MyModelView4(sqla.ModelView):
    can_view_details = True
    column_list = ["user_id","thread_id"]
    column_sortable_list = column_list
    def is_accessible(self):
        return not login.current_user.is_anonymous and login.current_user.is_admin
    
class MyModelView5(sqla.ModelView):
    can_view_details = True
    column_list = ["user_id","token"]
    column_sortable_list = column_list
    def is_accessible(self):
        return not login.current_user.is_anonymous and login.current_user.is_admin
    
UsersAdminView = MyModelView1(Users, db.session)
MessagesAdminView = MyModelView2(Messages, db.session)
ThreadsAdminView = MyModelView3(Threads, db.session)
UserAccessAdminView = MyModelView4(UserAccess, db.session)
FCMTokenAdminView = MyModelView5(FCMToken, db.session)

admin.add_view(UsersAdminView)
admin.add_view(MessagesAdminView)
admin.add_view(ThreadsAdminView)
admin.add_view(UserAccessAdminView)
admin.add_view(FCMTokenAdminView)

cred = credentials.Certificate("../key_firebase/bbs-app-da21d-firebase-adminsdk-r05g1-9ba685c39b.json")
firebase_admin.initialize_app(cred)
from models import UserAccess,FCMToken
def send_notification(data):
    push_users = UserAccess.query.filter(UserAccess.thread_id == data['thread_id'])
    users_id = [push_user.user_id for push_user in push_users if push_user.user_id !=data['send_user']]
    fcm_users=FCMToken.query.filter(FCMToken.user_id.in_(users_id)).all()
    fcm_tokens=[fcm_user.token for fcm_user in fcm_users]
    message = messaging.MulticastMessage(
        data={
            'score': '850', 
            'time': '2:45',
        },
        notification = messaging.Notification(
            title=data['title'],
            body=data['body'],
        ),
        tokens=fcm_tokens,
    )
    response = messaging.send_multicast(message)
    return jsonify({'success': True, 'response': response.success_count})