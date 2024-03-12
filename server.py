from web_app_BBS.main import app,socketio
# from web_app_BBS.main import app,socketio
from web_app_BBS.__init__ import app1,socketio
from flask import Flask,Blueprint
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker
import flask_login
from flask_wtf.csrf import CSRFProtect
from web_app_BBS.config import Config

# from app2.views import app2
# app.register_blueprint(app2, url_prefix='/app2')
app1.register_blueprint(app, url_prefix='/web_app_bbs')
if __name__ == '__main__':
    socketio.run(app1,debug=True,host="0.0.0.0",port=3000)
