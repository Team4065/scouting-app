from flask import Flask, render_template, request
from datetime import datetime as dt
import logging
import dotenv
import os

from .auth.models import User
from .auth.validators import allow_if
from .extensions import register_extensions

dotenv.load_dotenv('.env', verbose=True) # Load environment variables from .env

def create_app(config_object='app.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
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

    @app.after_request
    def after_request(response):
        """ Logging after every request. """
        logger = logging.getLogger("app.access")
        logger.info(
            "%s [%s] %s %s %s %s %s %s %s",
            request.remote_addr,
            dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.scheme,
            response.status,
            response.content_length,
            request.referrer,
            request.user_agent,
        )
        return response

    return app

    return app