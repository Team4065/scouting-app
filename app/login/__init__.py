from flask import Blueprint

login_blueprint = Blueprint('login', __name__)

from . import routes