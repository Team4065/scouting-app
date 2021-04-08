from flask import Flask, render_template, url_for
import os
import dotenv
from flask import redirect
from flask.helpers import flash
from flask_login import LoginManager, login_required, current_user
from .database import users, get_user_by_email
from .auth.models import User
from .auth.validators import allow_if

dotenv.load_dotenv('.env', verbose=True) # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('secret_key') or os.urandom(32)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @app.route('/scout')
    @allow_if(['scout', 'admin'])
    def scout():
        return ''

    @app.route('/')
    @allow_if(['scout', 'admin'], flash_user=False)
    def index():
        return render_template('index.html')

    @app.route('/admin/')
    @allow_if(['admin'])
    def admin():
        return render_template("admin.html")

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
        data = get_user_by_email(user_id)
        if data is None:
            return None
        return User(**data, authenticated=False)
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('auth.login'))

    return app