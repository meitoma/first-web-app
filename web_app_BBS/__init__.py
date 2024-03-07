from flask import Flask,jsonify
import flask_login as login

from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
import flask_login
from flask_wtf.csrf import CSRFProtect
from web_app_BBS.config import Config
import sys
import os

app = Flask(__name__,static_folder='bbs', template_folder='bbs/templates')
app.config.from_object(Config)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
metadata = MetaData()
socketio = SocketIO(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
