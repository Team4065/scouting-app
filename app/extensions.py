from flask import redirect, url_for
from flask_login import LoginManager, login_manager
import os

from .database import get_user_by_email
from .auth.models import User

def register_blueprints(app):
  from .auth import auth_blueprint
  app.register_blueprint(auth_blueprint)
  from .api import api_blueprint
  app.register_blueprint(api_blueprint)
  from .admin import admin_blueprint
  app.register_blueprint(admin_blueprint)

def register_login_manager(app):

  login_manager = LoginManager()
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id):
    data = get_user_by_email(user_id)
    if data is None:
      return None
    return User(**data, authenticated=False)
    
  @login_manager.unauthorized_handler
  def unauthorized():
    return redirect(url_for('auth.login'))

def register_url_additions(app):
  @app.context_processor
  def override_url_for():
    return dict(url_for=dated_url_for)
      
  def dated_url_for(endpoint, **values):
    if endpoint == 'static':
      filename = values.get('filename', None)
      if filename:
        file_path = os.path.join(app.root_path, endpoint, filename)
        values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def register_extensions(app):
  register_login_manager(app)
  register_blueprints(app)
  register_url_additions(app)