from bbs_app.main import bbs_app
from bbs_app.__init__ import app,socketio

from flask import Flask,Blueprint
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
import flask_login
from flask_wtf.csrf import CSRFProtect
from bbs_app.config import Config

# from app2.views import app2
# app.register_blueprint(app2, url_prefix='/app2')
app.register_blueprint(bbs_app, url_prefix='/bbs_app')
if __name__ == '__main__':
    socketio.run(app,debug=True,host="0.0.0.0",port=3000)
