from flask import render_template

from ..auth.validators import allow_if
from . import admin_blueprint as admin

@admin.route('/')
@allow_if(['admin'])
def dashboard():
  return render_template('admin/dashboard.html')

@admin.route('/scouters')
@allow_if(['admin'])
def scouters():
  return render_template('admin/scouters.html')

@admin.route('/analytics')
@allow_if(['admin'])
def analytics():
  return render_template('admin/analytics.html')

@admin.route('/viewer')
@allow_if(['admin'])
def data_viewer():
  return render_template('admin/viewer.html')

@admin.route('/settings')
@allow_if(['admin'])
def settings():
  return render_template('admin/settings.html')

