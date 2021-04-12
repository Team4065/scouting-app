from flask import render_template

from ..auth.validators import allow_if
from . import scout_blueprint as scout

@scout.route('/')
@allow_if(['scout', 'admin'])
def dashboard():
  return render_template('scout.html')
