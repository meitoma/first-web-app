from flask import jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
import firebase_admin
from firebase_admin import credentials, messaging
import flask_login as login
from bbs_app.models import Users,Messages,Threads,UserAccess,FCMToken
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv


cred = credentials.Certificate("../key_firebase/bbs-app-da21d-firebase-adminsdk-r05g1-9ba685c39b.json")
firebase_admin.initialize_app(cred)
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

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path) #.envファイルの読み込み
YAHOO_CLIENT_KEY=os.environ.get("YAHOO_CLIENT_KEY")
def get_external_api_data(api_url):
    api_url+=YAHOO_CLIENT_KEY
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            api_data = response.json()
            print(api_data)
            return api_data
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None