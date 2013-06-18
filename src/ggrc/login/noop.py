"""ggrc.login.noop

Login as example user for development mode.
"""

import flask_login
import json
from flask import url_for, redirect, request, session

from ggrc.login.common import find_or_create_user_by_email, get_next_url


def get_user():
  if 'X-ggrc-user' in request.headers:
    json_user = json.loads(request.headers['X-ggrc-user'])
    email = json_user.get('email', 'user@example.com')
    name = json_user.get('name', 'Example User')
    permissions = json_user.get('permissions', ())
  else:
    email = 'user@example.com'
    name = 'Example User'
    permissions = None
  user = find_or_create_user_by_email(
    email=email,
    name=name)
  session['permissions'] = permissions
  return user

def login():
  user = get_user()
  flask_login.login_user(user)
  return redirect(get_next_url(request, default_url=url_for('dashboard')))

def logout():
  flask_login.logout_user()
  return redirect(get_next_url(request, default_url=url_for('index')))
