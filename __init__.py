from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import flask_login
from config import Config
import sys

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

import main, models