from flask import render_template

from . import admin_blueprint as admin

@admin.route('/')
def dashboard():
  return render_template('admin.html')
