from flask import Flask,Blueprint
from flask import flash, redirect, url_for,render_template,request,jsonify
from flask_login import (
        current_user, login_user, logout_user, login_required
    )
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room, rooms, disconnect      
from sqlalchemy import text
import csv
from __init__ import db,metadata,socketio,login_manager

from bbs_app.forms import LoginForm, SignupForm, MessageForm, NewThreadForm, DeleteForm, AddMmemberForm
from bbs_app.models import Users,Messages,Threads,UserAccess,FCMToken
from bbs_app.external_api import send_notification,get_external_api_data
import datetime
import secrets
from PIL import Image
from io import BytesIO
from zoneinfo import ZoneInfo
from urllib.parse import urlparse
import wcwidth
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
import time
import os
import sys

bbs_app = Blueprint('bbs_app', __name__, static_folder='bbs', template_folder='bbs/templates')
# print("main:",__name__)
in_threads=set()
@login_required
@bbs_app.route('/load_data')
def users_load():
    #? Users tableの内容削除
    db.drop_all()
    db.create_all()

    #? csvからUsersへの書き込み
    with open("bbs/csv/users.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_users=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            print(row)
            user=Users(name=row[0],password=row[1],admin=bool(int(row[2])))
            add_users.append(user)
        db.session.add_all(add_users)
        db.session.commit()
    return threads_load()

def threads_load():
    #? csvからUsersへの書き込み
    with open("bbs/csv/threads.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_threads=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            thread=Threads(thread_name=row[0])
            add_threads.append(thread)
        db.session.add_all(add_threads)
        db.session.commit()
    return user_access_load()

def user_access_load():
    #? csvからUsersへの書き込み
    with open("bbs/csv/user_access.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_useraccess=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            useraccess=UserAccess(user_id=row[0],thread_id=row[1])
            add_useraccess.append(useraccess)
        db.session.add_all(add_useraccess)
        db.session.commit()
    return messages_load()

def messages_load():
    message = "Data loading completed"
    #? csvからMessageへの書き込み
    with open("bbs/csv/message.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_message=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            tdatetime = datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
            messages=Messages(user_id=row[0],thread_id=row[1],message_type=row[2],message=row[3],sendtime=tdatetime)
            add_message.append(messages)
        db.session.add_all(add_message)
        db.session.commit()

    data=[db.session.query(Users).all(),
          db.session.query(Messages).all(),
          db.session.query(Threads).all(),
          db.session.query(UserAccess).all()]
    return render_template('bbs_app/comp_load.html', message = message,data=data)

def count_characters(text):
    return sum(wcwidth.wcwidth(char) if wcwidth.wcwidth(char) > 0 else 1 for char in text)

# 画像アップロードの関数
def save_picture(form_picture,image_orientation):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'bbs/static/send_images', picture_fn)
    i = Image.open(form_picture)
    i_orientation = "vertical" if i.size[0]<i.size[1] else "horizontal"
    # print("receive:",image_orientation,"calc:",i_orientation)
    if image_orientation != i_orientation:
        i = i.rotate(-90, expand=True)
    i.thumbnail((800, 800))
    i.save(picture_path)
    return picture_fn

@bbs_app.route('/bbs/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def bbs(thread_id):
    thread = Threads.query.get(thread_id)
    title = thread.thread_name or request.args.get('title')
    users = Users.query.all()
    id_members= {user.id:user.name for user in users}
    form = MessageForm()
    if request.method == "POST":
        if form.validate_on_submit():
            current_time = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
            send_user = current_user.id
            send_time = current_time
            if form.image.data:
                picture_file = save_picture(form.image.data,request.form["image_orientation"])
                message_type = "image"
                my_message = picture_file
                notification_txt="画像が送信されました"
                user_message = Messages(user_id=send_user,message_type=message_type,message=my_message,sendtime=current_time,thread_id=thread_id)
                emit('add_meddage',{'type': message_type,"message":my_message,"messages_count":count_characters(my_message),"send_user":send_user,"send_time":send_time,"send_user_name":id_members[send_user]},namespace="/",to=str(thread_id))
            else:
                message_type="text"
                my_message = form.message.data
                notification_txt=my_message
                user_message = Messages(user_id=send_user,message_type=message_type,message=my_message,sendtime=current_time,thread_id=thread_id)
            db.session.add(user_message)
            db.session.commit()
            # db.session.close()
            send_notification({"thread_id":thread_id,"title":title,"body":notification_txt,"send_user":send_user})
            # time.sleep(10)
        return ('', 204)
        return redirect(url_for('bbs',thread_id=thread_id))
    else:
        user_access=UserAccess.query.filter(UserAccess.user_id == current_user.id)
        accessible_threads=set([ua.thread_id for ua in user_access])
        if thread_id not in accessible_threads or thread is None : return redirect(url_for('bbs_app.home',title="アクセス権がありません"))
        messages = Messages.query.filter(Messages.thread_id == thread_id)
        messages_count = [count_characters(message.message)for message in messages] #半角1,全角2でカウント
        members=[user.name for user in users]
        add_member = AddMmemberForm(members=members)
        new_thread_form = NewThreadForm(members=members)
        delete_form = DeleteForm()
        new_thread_form.process([])
        return render_template('bbs_app/bbs.html', title = title, thread_id=thread_id, user_access=user_access, current_user=current_user,messages=messages,messages_count=messages_count,form=form,add_member=add_member,new_thread_form=new_thread_form, delete_form=delete_form)

@bbs_app.route('/bbs/add_member', methods=['POST'])
@login_required
def add_member():
    users = Users.query.all()
    members=[user.name for user in users]
    add_member_form = AddMmemberForm(members=members)
    if add_member_form.validate_on_submit():
        thread_id=request.args.get('previous_thread')
        user_access=[UserAccess(user_id=int(m),thread_id=thread_id) for m in add_member_form.member.data]
        print(add_member_form.member.data)
        db.session.add_all(user_access)
        db.session.commit()
        db.session.close()
        print("in_threads",in_threads,request.args.get('previous_thread'))
        if in_threads:emit('reload', namespace="/",to=list(in_threads))
    return redirect(url_for('bbs_app.bbs',thread_id=thread_id))

@bbs_app.route('/bbs/new', methods=['POST'])
@login_required
def new_thread():
    users = Users.query.all()
    members=[user.name for user in users]
    new_thread_form = NewThreadForm(members=members)
    if new_thread_form.validate_on_submit():
        new_thread = Threads(thread_name=new_thread_form.thread_name.data)
        db.session.add(new_thread)
        db.session.flush()
        new_thread_id = new_thread.id
        user_access=[UserAccess(user_id=int(m),thread_id=new_thread_id) for m in new_thread_form.new_member.data]
        db.session.add_all(user_access)
        db.session.commit()
        db.session.close()
        if in_threads:emit('reload', namespace="/",to=list(in_threads))
        return redirect(url_for('bbs_app.bbs',thread_id=new_thread_id))
    return redirect(url_for('bbs_app.bbs',thread_id=request.args.get('previous_thread')))

@bbs_app.route('/bbs/delete', methods=['POST'])
@login_required
def delete_thread():
    delete_thread=request.args.get('delete_thread')
    delete_form = DeleteForm()
    current_thread=request.referrer.split('/')[-1]
    if delete_form.radio_field.data=="yes" and delete_thread == current_thread and delete_thread != "1":
        thread = Threads.query.filter_by(id=delete_thread).first()
        user_access_records = UserAccess.query.filter_by(thread_id=delete_thread).all()
        if thread and user_access_records:
            db.session.delete(thread)
            for user_access in user_access_records:
                db.session.delete(user_access)
            db.session.commit()
            emit('reload',namespace="/",to=list(in_threads))
        return redirect(url_for('bbs_app.home',title=f'"{thread.thread_name}"を削除しました'))
    else:
        return redirect(url_for('bbs_app.home',title=f'削除に失敗しました'))

@bbs_app.route('/bbs/home', methods=['GET','POST'])
@login_required
def home():
    title = request.args.get('title') or ""
    user_access=UserAccess.query.filter(UserAccess.user_id == current_user.id)
    users = Users.query.all()
    members=[user.name for user in users]
    new_thread_form = NewThreadForm(members=members)
    return render_template('bbs_app/home.html',title=title, user_access=user_access,new_thread_form=new_thread_form)

@bbs_app.route('/confirm')
@login_required
def confirm():
    if current_user.is_admin:
        title = "ログインユーザ一覧"
        users = Users.query.all()
        return render_template('bbs_app/confirm.html', title = title, current_user=current_user,users=users)
    else:
        return redirect(url_for('bbs_app.bbs',thread_id=1))

@bbs_app.route('/', methods=['GET', 'POST'])
@bbs_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bbs_app.bbs',thread_id=1))
    form = LoginForm()
    signup_form = SignupForm()
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    if form.validate_on_submit():
        # name:test, pass:test
        user = Users.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('ユーザーネームもしくはパスワードが正しくありません','failed')
            return redirect(url_for('bbs_app.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('bbs_app.bbs',thread_id=1)
        return redirect(next_page)
    return render_template('bbs_app/login.html',form=form,signup_form=signup_form,default_login="block",default_signup="none",next_page=request.args.get('next'))    

@bbs_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('bbs_app.login'))

@bbs_app.route('/signup', methods=['POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('bbs_app.bbs',thread_id=1))
    login_form = LoginForm()
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        print(f"in:{signup_form.name.data}")
        user = Users(name=signup_form.name.data ,password=signup_form.password.data)
        user.add_user()
        return redirect(url_for('bbs_app.login'))
    return render_template('bbs_app/login.html', form=login_form,signup_form=signup_form,default_login="none",default_signup="block",next_page=request.args.get('next'))

# adminページ
admin = Admin(
    bbs_app,
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


# socket通信
@socketio.on('submit_message')
def handle_submit_message(data):
    users = Users.query.all()
    id_members= {user.id:user.name for user in users}
    current_time = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    send_user = int(current_user.id)
    thread_id = data["thread_id"]
    send_time = current_time
    message_type="text"
    my_message = data["message"]
    emit('add_meddage',{'type': message_type,"message":my_message,"messages_count":count_characters(my_message),"send_user":send_user,"send_time":send_time,"send_user_name":id_members[send_user]},namespace="/",to=str(thread_id))

@socketio.on('set_notification')
def handle_set_notification(data):
    print(data["token"],data["user_id"])
    if not FCMToken.query.filter_by(token=data["token"]).one_or_none():
        fcm_token=FCMToken(token=data["token"],user_id=data["user_id"])
        db.session.add(fcm_token)
        db.session.commit()
        db.session.close()

@socketio.on('join')
def handle_join(data):
    room = data["room"]
    in_threads.add(room)
    join_room(room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)

@socketio.on('get_reverse_geo')
def handle_get_reverse_geo(data):
    lat,lon=data['latitude'],data['longitude']
    external_api_url = f"https://map.yahooapis.jp/geoapi/V1/reverseGeoCoder?lat={lat}&lon={lon}&output=json&appid="
    result = get_external_api_data(external_api_url)
    print(result)

