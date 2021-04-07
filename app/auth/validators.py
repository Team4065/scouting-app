from firebase_admin import auth
import flask
from flask.globals import session
from ..database import users

def get_token_from_context(ctx):
  try:
    token = auth.verify_session_cookie(ctx.cookies.get('session'), check_revoked=True)
    return token
  except Exception:
    return None

def is_admin(ctx):
  token = get_token_from_context(ctx)
  if token and token.get('admin'):
    return True
  return False


def get_role(ctx):
  """ Will return the role of the uuid assosiated with the current user, None if no user logged in. """
  token = get_token_from_context(ctx)
  if not token:
    return None

  uid = token['user_id']
  user = users.document(uid).get()

  if not user.exists:
    return None

  return user.to_dict()['role']
