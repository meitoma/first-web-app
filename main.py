from flask import Flask
from flask import flash, redirect, url_for,render_template,request
from flask_login import (
        current_user, login_user, logout_user, login_required
    )
from sqlalchemy import text
import csv
from __init__ import app,db,metadata
from forms import LoginForm,SignupForm,PostForm
from models import Users,Messages
import datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlparse
from __init__ import login_manager


@app.route('/load_data')
def users_load():
    message = "Users loading completed"
    #? Users tableの内容削除
    db.drop_all()
    db.create_all()

    #? csvからUsersへの書き込み
    with open("csv/users.csv","r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        add_users=[]
        next(reader) #csvファイルの1行目(列名)を除く
        for row in reader:
            user=Users(name=row[0],password=row[1])
            add_users.append(user)
        db.session.add_all(add_users)
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
            messages=Messages(user_id=row[0],message=row[1])
            add_message.append(messages)
        db.session.add_all(add_message)
        db.session.commit()
    data1=db.session.query(Users).all()
    data2=db.session.query(Messages).all()
    return render_template('comp_load.html', message = message,data1=data1,data2=data2)

@app.route('/bbs/1', methods=['GET', 'POST'])
@login_required
def bbs():
    title = "掲示板"
    messages = Messages.query.all()
    form = PostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            current_time = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
            user_message = Messages(user_id=current_user.id,message=form.message.data,sendtime=current_time)
            db.session.add(user_message)
            db.session.commit()
            db.session.close()
        return redirect(url_for('bbs'))
    else:
        return render_template('bbs.html', title = title, current_user=current_user.id,messages=messages,form=form)
    
@app.route('/confirm')
@login_required
def confirm():
    title = "ユーザ一覧"
    users = Users.query.all()
    return render_template('confirm.html', title = title, current_user=current_user.id,users=users)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bbs'))
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
            next_page = url_for('bbs')
        return redirect(next_page)
    return render_template('login.html', title='ログイン', form=form, develop=app.config['DEBUG'],next_page=request.args.get('next'))
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('bbs'))
    form = SignupForm()
    if request.method == "POST":
        print(form.name.data)
        if form.validate_on_submit():
            print(f"in:{form.name.data}")
            user = Users(name=form.name.data ,password=form.password.data)
            user.add_user()
            return redirect(url_for('login'))
    return render_template('signup.html', title='新規登録', form=form)



