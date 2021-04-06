from flask import Flask, render_template, url_for
import os
import dotenv
from app.database import db
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
from .database import users
import json

dotenv.load_dotenv('.env', verbose=True) # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    login_manager = LoginManager()
    login_manager.init_app(app)

    with open('credentials.json') as cred:
        google_client_id = json.load(cred)
        client = WebApplicationClient(google_client_id['client_id'])

    @app.route('/')
    def index():
        return 'Nothing to see here!'

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
        users.document

    return app