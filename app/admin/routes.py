from flask import render_template

from ..auth.validators import allow_if
from . import admin_blueprint as admin

@admin.route('/')
@allow_if(['admin'])
def dashboard():
  return render_template('admin.html')
