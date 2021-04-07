from firebase_admin import auth
from flask import current_app, flash
from functools import wraps
from flask_login import current_user

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

def allow_if(authorized_roles: list[str]):
  def decorator(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
      if not (current_user.is_authenticated and current_user.role in authorized_roles):
        return current_app.login_manager.unauthorized()
      return fn(*args, **kwargs)
    return decorated_view
  return decorator
