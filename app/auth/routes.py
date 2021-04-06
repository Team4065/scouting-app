from flask import request, render_template, redirect, abort
from flask.helpers import url_for
from flask.wrappers import Response
from firebase_admin.auth import verify_id_token
from . import auth_blueprint as auth
from ..database import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        resp = request.get_json()
        if resp == None:
            abort(400) # Header wasn't formatted correctly for json
        token = resp['auth_token']['token']
        decoded_token = verify_id_token(token)
        uid = decoded_token['uid']
        print(uid)
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    return redirect('/')
