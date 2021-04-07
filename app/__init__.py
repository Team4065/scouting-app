from flask import Flask, render_template
from markupsafe import escape
import dotenv
from app.database import db

dotenv.load_dotenv('.env', verbose=True) # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def scout():
        return render_template("scout.html")

    @app.route('/about/')
    def about():
        return render_template("about.html")

    @app.route('/admin/')
    def admin():
        return render_template("admin.html")

    from .login import login_blueprint
    app.register_blueprint(login_blueprint)

    return app