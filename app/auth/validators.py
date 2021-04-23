from firebase_admin import auth
from flask import current_app, flash, request
from functools import wraps
from flask_login import current_user, logout_user
from firebase_admin.auth import verify_session_cookie, InvalidSessionCookieError

def get_token_from_context(ctx):
  try:
    cookie = ctx.cookies.get('auth_token')
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

def allow_if(authorized_roles: list[str], flash_user=True):
  def decorator(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
      session_cookie = request.cookies.get('auth_token')
      if session_cookie:
        try:
          decoded = verify_session_cookie(session_cookie, check_revoked=True)
        except InvalidSessionCookieError as e:
          logout_user()
          flash('Invalid session cookie!')
      else:
        flash('Failed to retrieve a session. Logging out. . .')
        logout_user()
        return current_app.login_manager.unauthorized()

      if not (current_user.is_authenticated or (hasattr(current_user, 'role') and current_user.role in authorized_roles)):
        if flash_user:
          flash('You are not authorized to view that page, redirecting.')
        return current_app.login_manager.unauthorized()

      return fn(*args, **kwargs)
    return decorated_view
  return decorator
