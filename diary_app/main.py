from flask import Flask,Blueprint
from flask import flash, redirect, url_for,render_template,request,jsonify

import time
import os
import sys

diary_app = Blueprint('diary_app', __name__, static_folder='diary', template_folder='diary/templates')

@diary_app.route('/', methods=['GET', 'POST'])
@diary_app.route('/diary')
def diary():
    return render_template('diary_app/home_copy.html')    

