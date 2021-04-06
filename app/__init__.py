from flask import Flask, render_template, url_for
import os
import dotenv
from flask.globals import request
from flask_login import login_required
from app.database import db
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
from .database import users
from .auth.models import User
# from .auth.validators import is_auth, get_role, user_exists
import json

dotenv.load_dotenv('.env', verbose=True) # Load environment variables from .env
dotenv.load_dotenv('.env.prod', verbose=True) # Load production environment variables from .env.prod

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('secret_key') or os.urandom(32)

    login_manager = LoginManager()
    login_manager.init_app(app)

    with open('credentials.json') as cred:
        google_client_id = json.load(cred)
        client = WebApplicationClient(google_client_id['client_id'])

    @app.route('/')
    def index():
        if is_auth(request_ctx=request):
            print(get_role(request_ctx=request))
            return 'You are authorized to view this content.'
        else:
            return 'You are not authorized to view this content. Click <a href="/auth/login">here</a> to login.'

    @app.route('/secret')
    @login_required
    def secret():
        return 'Secret page!'

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)

    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path,
                                    endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)

    @login_manager.user_loader
    def load_user(user_id):
        return User(**users.document(user_id).get().to_dict())

    return app