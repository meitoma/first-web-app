from flask import Flask,Blueprint,session
from flask import flash, redirect, url_for,render_template,request,jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room, rooms, disconnect      
from sqlalchemy import text
import csv
from __init__ import db,metadata,socketio,login_manager,app

from bbs_app.forms import LoginForm, SignupForm, MessageForm, NewThreadForm, DeleteForm, AddMmemberForm
from bbs_app.models import Users,Messages,Threads,UserAccess,FCMToken,WorkSpaces,WSAccessUser
from bbs_app.external_api import send_notification,get_external_api_data
import bbs_app.my_admin
import datetime
import secrets
from PIL import Image
from io import BytesIO
from zoneinfo import ZoneInfo
from urllib.parse import urlparse
import wcwidth
import time
import os
import sys

token=secrets.token_hex(16)
print("token",token)
bbs_app = Blueprint('bbs_app', __name__, static_folder='bbs', template_folder='bbs/templates')

# print("main:",__name__)
in_threads=set()
@login_required
@bbs_app.route('/<string:ws_name>/load_data')
def users_load(ws_name):
    #? Users tableの内容削除
    db.drop_all()
    db.create_all()

    #? csvからUsersへの書き込み
    with open("bbs_app/bbs/csv/users.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_users=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            user=Users(name=row[0],password=row[1],admin=bool(int(row[2])))
            add_users.append(user)
        db.session.add_all(add_users)
        db.session.commit()
    return workspaces_load(ws_name)

def workspaces_load(ws_name):
    #? csvからWorkSpacesへの書き込み
    with open("bbs_app/bbs/csv/workspaces.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_workspaces=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            print(row)
            tdatetime = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            workspaces=WorkSpaces(ws_name=row[0],ws_token=row[1],update_time=tdatetime)
            add_workspaces.append(workspaces)
        db.session.add_all(add_workspaces)
        db.session.commit()
    return workspace_access_load(ws_name)

def workspace_access_load(ws_name):
    #? csvからWSAccessUserへの書き込み
    with open("bbs_app/bbs/csv/ws_access.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_wsaccess=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            ws_access=WSAccessUser(user_id=row[0],ws_id=row[1])
            add_wsaccess.append(ws_access)
        db.session.add_all(add_wsaccess)
        db.session.commit()
    return threads_load(ws_name)

def threads_load(ws_name):
    #? csvからUsersへの書き込み
    with open("bbs_app/bbs/csv/threads.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_threads=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            thread=Threads(thread_name=row[0],ws_id=row[1])
            add_threads.append(thread)
        db.session.add_all(add_threads)
        db.session.commit()
    return user_access_load(ws_name)

def user_access_load(ws_name):
    #? csvからUsersへの書き込み
    with open("bbs_app/bbs/csv/user_access.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_useraccess=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            useraccess=UserAccess(user_id=row[0],thread_id=row[1])
            add_useraccess.append(useraccess)
        db.session.add_all(add_useraccess)
        db.session.commit()
    return messages_load(ws_name)

def messages_load(ws_name):
    message = "Data loading completed"
    #? csvからMessageへの書き込み
    with open("bbs_app/bbs/csv/message.csv","r",encoding="utf-8") as csvfile:
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
    return render_template('bbs_app/comp_load.html',ws_name=ws_name, message = message,data=data)

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

def get_jinja_variable(ws_name):
    user_access=UserAccess.query.filter(UserAccess.user_id == current_user.id)
    work_space = WorkSpaces.query.filter(WorkSpaces.ws_name == ws_name).first()
    accessible_ws = WSAccessUser.query.filter(WSAccessUser.user_id == current_user.id)
    accessible_ws = set([wa.ws_id for wa in accessible_ws])
    ws_has_users = WSAccessUser.query.filter(WSAccessUser.ws_id == work_space.id)
    ws_has_users = set([ws_has_user.id for ws_has_user in ws_has_users])
    ws_has_threads = Threads.query.filter(Threads.ws_id == work_space.id)
    ws_has_threads = set([ws_has_thread.id for ws_has_thread in ws_has_threads])
    users = Users.query.all()
    members=[user.name for user in users if user.id in ws_has_users]
    new_thread_form = NewThreadForm(members=members)
    jinja_variable={"user_access":user_access,"work_space":work_space,"accessible_ws":accessible_ws,"ws_has_users":ws_has_users,"ws_has_threads":ws_has_threads,"new_thread_form":new_thread_form,"members":members}
    return jinja_variable

@bbs_app.route('/bbs/<string:ws_name>/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def bbs(ws_name,thread_id):
    thread = Threads.query.get(thread_id)
    if thread is None:return redirect(url_for('bbs_app.home',ws_name=ws_name,title="アクセス権がありません"))
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
        jv = get_jinja_variable(ws_name)
        if jv["work_space"] is None or jv["work_space"].id not in jv["accessible_ws"] or thread is None or thread.ws_id != jv["work_space"].id:return redirect(url_for('bbs_app.home',ws_name=ws_name,title="アクセス権がありません"))
        
        user_access=UserAccess.query.filter(UserAccess.user_id == current_user.id)
        accessible_threads=set([ua.thread_id for ua in user_access])

        if thread_id not in accessible_threads: return redirect(url_for('bbs_app.home',ws_name=ws_name,title="アクセス権がありません"))
        messages = Messages.query.filter(Messages.thread_id == thread_id)
        messages_count = [count_characters(message.message)for message in messages] #半角1,全角2でカウント
        add_member = AddMmemberForm(members=jv["members"])
        delete_form = DeleteForm()
        return render_template('bbs_app/bbs.html', title = title, thread_id=thread_id, work_space=jv["work_space"],user_access=user_access, ws_has_threads=jv["ws_has_threads"],current_user=current_user,messages=messages,messages_count=messages_count,form=form,add_member=add_member,new_thread_form=jv["new_thread_form"], delete_form=delete_form)

@bbs_app.route('/bbs/<string:ws_name>/home', methods=['GET','POST'])
@login_required
def home(ws_name):
    title = request.args.get('title') or ""
    jv = get_jinja_variable(ws_name)
    if jv["work_space"] is None or jv["work_space"].id not in jv["accessible_ws"]:return "アクセス権がありません"
    return render_template('bbs_app/home.html',title=title, user_access=jv["user_access"], ws_has_threads=jv["ws_has_threads"],ws_has_users=jv["ws_has_users"], work_space=jv["work_space"],new_thread_form=jv["new_thread_form"])

@bbs_app.route('/invite/<string:ws_name>/<string:ws_token>', methods=['GET'])
def invite(ws_name,ws_token):
    work_space = WorkSpaces.query.filter(WorkSpaces.ws_name == ws_name).first()
    if work_space is None or not secrets.compare_digest(ws_token, work_space.ws_token):return "URLが無効です"
    ws_access = WSAccessUser.query.filter(WSAccessUser.ws_id == work_space.id)
    accessible_ws = set([wa.user_id for wa in ws_access])
    if current_user.id not in accessible_ws:
        add_ws_access = WSAccessUser(user_id=current_user.id,ws_id=work_space.id)
        db.session.add(add_ws_access)
        db.session.commit()
        db.session.close()
        return redirect(url_for('bbs_app.home',ws_name=ws_name,title="登録しました"))
    else:
        return redirect(url_for('bbs_app.home',ws_name=ws_name,title="すでに登録されています"))

@login_manager.unauthorized_handler
def unauthorized_callback():
    ws_name=request.path.split("/")[-2]
    session['next_url'] = request.path
    return redirect(url_for('bbs_app.login',ws_name=ws_name))

@bbs_app.route('/<string:ws_name>/', methods=['GET', 'POST'])
@bbs_app.route('/<string:ws_name>/login', methods=['GET', 'POST'])
def login(ws_name):
    if current_user.is_authenticated:
        return redirect(url_for('bbs_app.bbs',ws_name=ws_name,thread_id=0))

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
            return redirect(url_for('bbs_app.login',ws_name=ws_name))
        login_user(user)
        next_page = session.pop('next_url')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('bbs_app.bbs',ws_name=ws_name,thread_id=0)
        return redirect(next_page)
    return render_template('bbs_app/login.html',form=form,signup_form=signup_form,default_login="block",ws_name=ws_name,default_signup="none",next_page=request.args.get('next'))    

@bbs_app.route('/<string:ws_name>/logout')
def logout(ws_name):
    logout_user()
    return redirect(url_for('bbs_app.login',ws_name=ws_name))

@bbs_app.route('/<string:ws_name>/signup', methods=['POST'])
def signup(ws_name):
    if current_user.is_authenticated:
        return redirect(url_for('bbs_app.bbs',ws_name=ws_name,thread_id=1))
    login_form = LoginForm()
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        print(f"in:{signup_form.name.data}")
        user = Users(name=signup_form.name.data ,password=signup_form.password.data)
        user.add_user()
        return redirect(url_for('bbs_app.login',ws_name=ws_name))
    return render_template('bbs_app/login.html', form=login_form,signup_form=signup_form,default_login="none",default_signup="block",next_page=request.args.get('next'))

@bbs_app.route('/bbs/<string:ws_name>/add_member', methods=['POST'])
@login_required
def add_member(ws_name):
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
    return redirect(url_for('bbs_app.bbs',ws_name=ws_name,thread_id=thread_id))

@bbs_app.route('/bbs/<string:ws_name>/new', methods=['POST'])
@login_required
def new_thread(ws_name):
    users = Users.query.all()
    members=[user.name for user in users]
    new_thread_form = NewThreadForm(members=members)
    if new_thread_form.validate_on_submit():
        work_space = WorkSpaces.query.filter(WorkSpaces.ws_name == ws_name).first()
        new_thread = Threads(thread_name=new_thread_form.thread_name.data,ws_id=work_space.id)
        db.session.add(new_thread)
        db.session.flush()
        new_thread_id = new_thread.id
        user_access=[UserAccess(user_id=int(m),thread_id=new_thread_id) for m in new_thread_form.new_member.data]
        db.session.add_all(user_access)
        db.session.commit()
        db.session.close()
        if in_threads:emit('reload', namespace="/",to=list(in_threads))
        return redirect(url_for('bbs_app.bbs', ws_name=ws_name,thread_id=new_thread_id))
    return redirect(url_for('bbs_app.bbs', ws_name=ws_name, thread_id=request.args.get('previous_thread')))

@bbs_app.route('/bbs/<string:ws_name>/delete', methods=['POST'])
@login_required
def delete_thread(ws_name):
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
        return redirect(url_for('bbs_app.home',ws_name=ws_name,title=f'"{thread.thread_name}"を削除しました'))
    else:
        return redirect(url_for('bbs_app.home',ws_name=ws_name,title=f'削除に失敗しました'))

@bbs_app.route('/<string:ws_name>/confirm')
@login_required
def confirm(ws_name):
    if current_user.is_admin:
        title = "ログインユーザ一覧"
        users = Users.query.all()
        return render_template('bbs_app/confirm.html', title = title, current_user=current_user,users=users)
    else:
        return redirect(url_for('bbs_app.bbs',ws_name=ws_name,thread_id=1))  


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
