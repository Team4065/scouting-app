from flask import render_template

from ..auth.validators import allow_if
from . import scout_blueprint as scout

@scout.route('/')
@allow_if(['scout'])
def dashboard():
  return render_template('scout/dashboard.html')
