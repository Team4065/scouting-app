from flask import render_template, request, Response

from ..auth.validators import allow_if
from . import scout_blueprint as scout

@scout.route('/', methods=['GET'])
@allow_if(['scout'])
def dashboard():
  return render_template('scout/dashboard.html')

@scout.route('/submit', methods=['POST'])
@allow_if(['scout'])
def submit():
  # req = request.get_json()
  print('Submission!\n'*10)
  return Response(status=200)
