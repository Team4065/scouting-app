from flask import Blueprint

scout_blueprint = Blueprint('scout', __name__, url_prefix='/scout')

from . import routes