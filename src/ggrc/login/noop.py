"""ggrc.login.noop

Login as example user for development mode.
"""

import flask_login
from flask import url_for, redirect, request

from ggrc.login.common import find_or_create_user_by_email, get_next_url


def get_user():
  email = 'user@example.com'
  name = 'Example User'
  user = find_or_create_user_by_email(
    email=email,
    name=name)
  return user

def login():
  user = get_user()
  flask_login.login_user(user)
  return redirect(get_next_url(request, default_url=url_for('dashboard')))

def logout():
  flask_login.logout_user()
  return redirect(get_next_url(request, default_url=url_for('index')))
