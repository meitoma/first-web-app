from flask import Flask
import flask_login as login

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
import flask_login
from flask_wtf.csrf import CSRFProtect
from config import Config
import sys

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
metadata = MetaData()

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import Users,Messages
admin = Admin(
    app,
    name='Flask-admin laboratory',
    template_mode='bootstrap4',
)
class MyModelView(sqla.ModelView):
  def is_accessible(self):
    return not login.current_user.is_anonymous and login.current_user.is_admin

admin.add_view(MyModelView(Users, db.session))
admin.add_view(MyModelView(Messages, db.session))