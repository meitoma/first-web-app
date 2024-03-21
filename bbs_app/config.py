import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import timedelta
 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path) #.envファイルの読み込み

    USER_NAME=os.environ.get("USER_NAME")
    PASSWORD=os.environ.get("PASSWORD")
    HOSTNAME=os.environ.get("HOSTNAME")
    DB_NAME=os.environ.get("DB_NAME")
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_PORT=os.environ.get("DB_PORT") or ''
    PERMANENT_SESSION_LIFETIME = timedelta(days=1) #session time（1分）
    port=1000
    SQLALCHEMY_DATABASE_URI=f'postgresql://{USER_NAME}:{PASSWORD}@{HOSTNAME}{DB_PORT}/{DB_NAME}'
    print(SQLALCHEMY_DATABASE_URI)
    # SQLALCHEMY_DATABASE_URI=f'postgresql://{USER_NAME}@{HOSTNAME}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def test_postges(USER_NAME,PASSWORD,HOSTNAME,DB_NAME):
        # この方法でも接続できるらしい　未確認
        CONNECT_STR=f'postgresql://{USER_NAME}:{PASSWORD}@{HOSTNAME}/{DB_NAME}'
        ENGINE = create_engine(CONNECT_STR)
        SESSION = sessionmaker(ENGINE)
        local_session=SESSION()