from datetime import datetime
from flask import request, render_template, redirect, abort, flash, jsonify, make_response
from flask_login import login_user, logout_user, current_user
from firebase_admin.exceptions import FirebaseError
from flask.helpers import url_for
import datetime
from firebase_admin.auth import create_session_cookie, verify_id_token, verify_session_cookie, revoke_refresh_tokens, InvalidSessionCookieError
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


        expires_in = datetime.timedelta(minutes=5)
        try:
            session_cookie = create_session_cookie(token, expires_in=expires_in)
            response = jsonify({'status': 'success'})
            expires = datetime.datetime.now() + expires_in
            response.set_cookie(
                'auth_token', value=session_cookie
            )
            return response
        except FirebaseError:
            return abort(401, 'Failed to create a session cookie!')

    elif request.method == 'GET':
        cookie = request.cookies.get('auth_token')
        print(f'Get Cookie: {cookie}')
        if cookie:
            try:
                decoded = verify_session_cookie(cookie, check_revoked=True)
                if not current_user.is_authenticated:
                    user = User(uid=decoded['user_id'], email=decoded['email'], role='default', authenticated=True)
                    login_user(user, remember=True)

                return redirect('/') # Session valid already, no reason to login
            except InvalidSessionCookieError as e:
                flash('Session expired. Please login again.')
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    session_cookie = request.cookies.get('auth_token')
    try:
        decoded_claims = verify_session_cookie(session_cookie)
        revoke_refresh_tokens(decoded_claims['sub'])
        response = make_response(redirect(url_for('auth.login')))
        response.set_cookie('session', value='', expires=0)
        return response
    except InvalidSessionCookieError:
        return redirect(url_for('auth.login'))

