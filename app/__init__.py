from flask import Flask, render_template
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

    return app