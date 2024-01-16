from flask import Flask
from flask import flash, redirect, url_for,render_template,request
from flask_login import (
        current_user, login_user, logout_user, login_required
    )
from __init__ import app
from forms import LoginForm,SignupForm
from models import Users

@app.route('/index')
@login_required
def index():
    message = "Job list"
    # jobs = Job.query.all()
    return render_template('view.html', message = message)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # if form.validate_on_submit():
    if request.method == "POST":
        # name:root, pass:root
        user = Users.query.filter_by(name=form.name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid name or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', title='Sign In', form=form)
    
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
    return render_template('signup.html', title='Sign Up', form=form)



