from flask import Flask
from flask import flash, redirect, url_for,render_template,request
from flask_login import (
        current_user, login_user, logout_user, login_required
    )
from flask_socketio import SocketIO, emit, join_room, leave_room, \
      close_room, rooms, disconnect      
from sqlalchemy import text
import csv
from __init__ import app,db,metadata,socketio
from forms import LoginForm, SignupForm, MessageForm, NewThreadForm, DeleteFort
from models import Users,Messages,Threads,UserAccess
import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlparse
from __init__ import login_manager
import time


@app.route('/load_data')
def users_load():
    #? Users tableの内容削除
    db.drop_all()
    db.create_all()

    #? csvからUsersへの書き込み
    with open("csv/users.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_users=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            user=Users(name=row[0],password=row[1],admin=bool(int(row[2])))
            add_users.append(user)
        db.session.add_all(add_users)
        db.session.commit()
    return threads_load()

def threads_load():
    #? csvからUsersへの書き込み
    with open("csv/threads.csv","r",encoding="utf-8") as csvfile:
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
    with open("csv/user_access.csv","r",encoding="utf-8") as csvfile:
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
    with open("csv/message.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_message=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            tdatetime = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
            messages=Messages(user_id=row[0],thread_id=row[1],message=row[2],sendtime=tdatetime)
            add_message.append(messages)
        db.session.add_all(add_message)
        db.session.commit()

    data=[db.session.query(Users).all(),
          db.session.query(Messages).all(),
          db.session.query(Threads).all(),
          db.session.query(UserAccess).all()]
    return render_template('comp_load.html', message = message,data=data)

@app.route('/bbs/<int:thread_id>', methods=['GET', 'POST'])
@login_required
@socketio.on('my_chat')
def bbs(thread_id):
    user_access=UserAccess.query.filter(UserAccess.user_id == current_user.id)
    accessible_threads=set([ua.thread_id for ua in user_access])
    thread = Threads.query.get(thread_id)
    if thread_id not in accessible_threads or thread is None : return redirect(url_for('home',title="アクセス権がありません"))

    title = thread.thread_name or request.args.get('title')
    messages = Messages.query.filter(Messages.thread_id == thread_id)
    
    form = MessageForm()
    users = Users.query.all()
    members=[user.name for user in users]
    new_thread_form = NewThreadForm(members=members)
    delete_form = DeleteFort()
    new_thread_form.process([])
    if request.method == "POST":
        if form.validate_on_submit():
            current_time = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
            user_message = Messages(user_id=current_user.id,message=form.message.data,sendtime=current_time,thread_id=thread_id)
            db.session.add(user_message)
            db.session.commit()
            db.session.close()
            emit('message', {'message': "data"},to=str(thread_id),namespace="/")
        return redirect(url_for('bbs',thread_id=thread_id))
    else:
        return render_template('bbs.html', title = title, thread_id=thread_id, user_access=user_access, current_user=current_user,messages=messages,form=form,new_thread_form=new_thread_form, delete_form=delete_form)

@app.route('/bbs/new', methods=['POST'])
@socketio.on('create_thread')
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
        user_access=[UserAccess(user_id=i+1,thread_id=new_thread_id) for i,m in enumerate(new_thread_form.member.data) if m]
        db.session.add_all(user_access)
        db.session.commit()
        db.session.close()
        emit('message', {'message': "create thread"},namespace="/")
        return redirect(url_for('bbs',thread_id=new_thread_id))
    return redirect(url_for('bbs',thread_id=request.args.get('previous_thread')))

@app.route('/bbs/delete', methods=['POST'])
@socketio.on('delete_thread')
@login_required
def delete_thread():
    delete_thread=request.args.get('delete_thread')
    delete_form = DeleteFort()
    current_thread=request.referrer.split('/')[-1]
    if delete_form.radio_field.data=="yes" and delete_thread == current_thread and delete_thread != 1:
        thread = Threads.query.filter_by(id=delete_thread).first()
        user_access_records = UserAccess.query.filter_by(thread_id=delete_thread).all()
        if thread and user_access_records:
            db.session.delete(thread)
            for user_access in user_access_records:
                db.session.delete(user_access)
            db.session.commit()
            emit('message', {'message': "delete thread"},namespace="/")
        return redirect(url_for('home',title=f'"{thread.thread_name}"を削除しました'))
    else:
        return redirect(url_for('home',title=f'削除に失敗しました'))

@app.route('/bbs/home', methods=['GET','POST'])
@login_required
def home():
    title = request.args.get('title') or ""
    user_access=UserAccess.query.filter(UserAccess.user_id == current_user.id)
    users = Users.query.all()
    members=[user.name for user in users]
    new_thread_form = NewThreadForm(members=members)
    return render_template('home.html',title=title, user_access=user_access,new_thread_form=new_thread_form)

@app.route('/bbs/not_found_bbs')
def not_found_bbs():
    return render_template('not_found_bbs.html')

@app.route('/confirm')
@login_required
def confirm():
    if current_user.is_admin:
        title = "ログインユーザ一覧"
        users = Users.query.all()
        return render_template('confirm.html', title = title, current_user=current_user,users=users)
    else:
        return redirect(url_for('bbs',thread_id=1))

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bbs',thread_id=1))
    form = LoginForm()
    if form.validate_on_submit():
        # name:test, pass:test
        user = Users.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('ユーザーネームもしくはパスワードが正しくありません','failed')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('bbs',thread_id=1)
        return redirect(next_page)
    return render_template('login.html', title='ログイン', form=form, develop=app.config['DEBUG'],next_page=request.args.get('next'))
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('bbs',thread_id=1))
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            print(f"in:{form.name.data}")
            user = Users(name=form.name.data ,password=form.password.data)
            user.add_user()
            return redirect(url_for('login'))
    return render_template('signup.html', title='新規登録', form=form)

# @socketio.on('connect')
# def handle_connect():
#     emit('client_echo',{'msg': 'server connected!'})

# @socketio.on('server_echo')
# def handle_server_echo(msg):
#     print('echo: ' + str(msg["data"]))

@socketio.on('join')
def handle_join(data):
    room = data["room"]
    join_room(room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)


