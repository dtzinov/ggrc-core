"""ggrc.login

Provides basic login and session management using Flask-Login with various
backends
"""

import flask_login
from .common import find_user_by_id

login_module = None

def get_login_module():
  global login_module
  if login_module is None:
    import sys
    from ggrc import settings
    login_module_name = settings.LOGIN_MANAGER

    if login_module_name:
      __import__(login_module_name)
      login_module = sys.modules[login_module_name]
    else:
      login_module = False
  return login_module

def user_loader(id):
  return find_user_by_id(id)

def init_app(app):
  login_module = get_login_module()
  if not login_module:
    return

  login_manager = flask_login.LoginManager()
  login_manager.init_app(app)
  login_manager.login_view = 'login'
  #login_manager.session_protection = 'strong'

  app.route('/login')(login_module.login)
  app.route('/logout')(login_module.logout)

  app.login_manager.user_loader(user_loader)
  #app.before_request(login_module.user_load_or_create)
  #app.context_processor(login_module.session_context)

def get_current_user():
  if get_login_module():
    return flask_login.current_user
  else:
    return None

def login_required(func):
  if get_login_module():
    return flask_login.login_required(func)
  else:
    return func
#login_required = flask_login.login_required
