from flask import jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
import firebase_admin
from firebase_admin import credentials, messaging
import flask_login as login
from web_app_BBS.__init__ import app,db
from web_app_BBS.models import Users,Messages,Threads,UserAccess,FCMToken

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