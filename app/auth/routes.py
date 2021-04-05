from flask import request, render_template, redirect
from flask.helpers import url_for
from . import auth_blueprint as auth
from ..database import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    return redirect('/')
