from flask import Flask
from markupsafe import escape
import dotenv
from app.database import db

dotenv.load_dotenv('.env', verbose=True) # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    @app.route('/', defaults={'id': ''})
    @app.route('/<id>')
    def hello_world(id=''):
        return f'Hello, Hunter! {id}'

    @app.route('/home')
    def home():
        return 'Home'

    from .login import login_blueprint
    app.register_blueprint(login_blueprint)

    return app