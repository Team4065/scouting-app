from flask import Flask, render_template, flash
import os
import dotenv

from .auth.models import User
from .auth.validators import allow_if
from .extensions import register_extensions

dotenv.load_dotenv('.env', verbose=True) # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get('secret_key') or os.urandom(32)

    register_extensions(app)

    @app.route('/scout')
    @allow_if(['scout', 'admin'])
    def scout():
        return ''

    @app.route('/')
    @allow_if(['default', 'scout', 'admin'], flash_user=False)
    def index():
        return render_template('index.html')

    @app.route('/admin/')
    @allow_if(['admin'])
    def admin():
        return render_template("admin.html")

    return app