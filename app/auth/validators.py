from firebase_admin import auth
from flask.globals import session
from ..database import users

def is_auth(request_ctx):
  session_cookie = request_ctx.cookies.get('session')
  if not session_cookie:
    return False
  return session_cookie

def is_admin(session_cookie):
  claims = auth.verify_session_cookie(session_cookie, check_revoked=False)
  if claims.get('admin') is True:
    return True
  return False

def get_role(request_ctx):
  session_cookie = request_ctx.cookies.get('session')
  uid = auth.verify_session_cookie(session_cookie)['user_id']

  user = users.document(uid).get()

  if not user.exists:
    return None

  return user.to_dict()['role']
