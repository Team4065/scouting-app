from datetime import datetime
from flask import request, render_template, redirect, abort, session, jsonify, make_response
from flask_login import login_user, logout_user, current_user
from firebase_admin.exceptions import FirebaseError
from flask.helpers import url_for
import datetime
from firebase_admin.auth import create_session_cookie, verify_id_token
from flask_login.utils import login_required
from .models import User
from . import auth_blueprint as auth
from ..database import add_user, user_exists

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        resp = request.get_json()
        if resp == None:
            abort(400) # Header wasn't formatted correctly for json
        token = resp['auth_token']
        decoded_token = verify_id_token(token)
        
        user = User(uid=decoded_token['user_id'], email=decoded_token['email'], role='default', authenticated=True)
        login_user(user, remember=True)

        if not user_exists(decoded_token['uid']):
            add_user(user)
            print('Adding user')


        expires_in = datetime.timedelta(days=1)
        try:
            session_cookie = create_session_cookie(token, expires_in=expires_in)
            response = jsonify({'status': 'success'})
            expires = datetime.datetime.now() + expires_in
            response.set_cookie(
                'session', session_cookie, expires=expires, httponly=True, secure=True
            )
            return response
        except FirebaseError:
            return abort(401, 'Failed to create a session cookie!')
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    print(current_user)

    response = make_response(redirect(url_for('auth.login')))
    response.set_cookie('session', expires=0)

    logout_user()

    return response
