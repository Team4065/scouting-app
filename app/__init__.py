from flask import Flask, render_template, url_for
import os
import dotenv
from app.database import db

dotenv.load_dotenv('.env', verbose=True) # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('base.html')

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

    return app