from firebase_admin import auth
import flask
from flask.globals import session
from ..database import users

def get_token_from_context(ctx):
  try:
    cookie = ctx.cookies.get('session')
    print(cookie)
    token = auth.verify_session_cookie(cookie, check_revoked=True)
    return token
  except Exception as e:
    print(e)
    return None

def is_admin(ctx):
  token = get_token_from_context(ctx)
  if token and token.get('admin'):
    return True
  return False