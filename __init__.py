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

# cred_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
cred = credentials.Certificate("./bbs/bbs-app-da21d-firebase-adminsdk-r05g1-9ba685c39b.json")
firebase_admin.initialize_app(cred)

def send_notification(data):
    registration_token=data['token']
    registration_token = 'e1kDniAELNpSkxS2DZUTFp:APA91bH4iQIqhVM_cBuzrAhc7potdWQWkt2hIrtX8AglRpZVDTgSuUfNouVN-5Dc_Dy-_kjWRcgV7SvboUQx1Vd1BlclC88BnY1pbJgCB_hUp4MXuKDMiUM84Ft-7_IhV5FpW-VWd6Oh'
    message = messaging.Message(
        notification=messaging.Notification(
            title=data['title'],
            body=data['body'],
        ),
        token=registration_token,
    )
    response = messaging.send(message)
    return jsonify({'success': True, 'response': response})