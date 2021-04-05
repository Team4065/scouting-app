from flask import request, render_template
from . import login_blueprint as login
from ..database import db

@login.route('/', methods=['POST'])
def index():
    email = request.form.get('email')

