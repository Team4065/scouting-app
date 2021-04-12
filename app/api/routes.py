from flask import json, jsonify

from . import api_blueprint as api
from ..auth.validators import allow_if
from ..database import get_users_by_role

@api.route('/status', methods=['GET'])
def status():
  return jsonify({ 'status': 'success' })

@api.route('/scout/all', methods=['GET'])
@allow_if(['admin'])
def get_all_scouts():
  scouts = get_users_by_role('scout')

  if len(scouts) < 1:
    return jsonify({ 'status': 'failed', 'reason': f'Failed to fetch scouts from database.' })

  return jsonify(scouts)

