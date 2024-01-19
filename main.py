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

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    title = "掲示板"
    messages = Messages.query.all()
    form = PostForm()
    if request.method == "POST":
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_message = Messages(user_id=current_user.id,message=form.message.data,time=current_time)
        db.session.add(user_message)
        db.session.commit()
        db.session.close()
        return redirect(url_for('index'))
    else:
        return render_template('index.html', title = title, current_user=current_user.id,messages=messages,form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # if form.validate_on_submit():
    if request.method == "POST":
        # name:test, pass:test
        user = Users.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('ユーザーネームもしくはパスワードが正しくありません','failed')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', title='ログイン', form=form, develop=app.config['DEBUG'])
    
@app.route('/logout')
def logout():
    logout_user()
    return render_template('logout.html', title='Log out')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if request.method == "POST":
        print(form.name.data)
        if form.validate_on_submit():
            print(f"in:{form.name.data}")
            user = Users(name=form.name.data ,password=form.password.data)
            user.add_user()
            return redirect(url_for('login'))
    return render_template('signup.html', title='新規登録', form=form)



