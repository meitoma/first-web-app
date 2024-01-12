from flask import Flask
from flask import flash, redirect, url_for,render_template,request
app = Flask(__name__)
@app.route('/')
def index():
    message = "hello flask"
    return render_template('index.html', message = message,)


