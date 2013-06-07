"""Login handler for using App Engine authentication with Flask-Login

Assumes app.yaml is configured with:

..
  handlers:
    - url: /login
      script: <wsgi_app path>
      login: required

E.g., ``login: required`` must be specified *at least* for the '/login' route.
"""

from google.appengine.api import users
from ggrc.login.common import find_or_create_user_by_email, get_next_url
import flask_login
from flask import url_for, redirect, request


def get_user():
  ae_user = users.get_current_user()
  email = ae_user.email()
  nickname = ae_user.nickname()
  user = find_or_create_user_by_email(email, name=nickname)
  return user

def login():
  user = get_user()
  flask_login.login_user(user)
  return redirect(
    get_next_url(request, default_url=url_for('dashboard')))
  #return redirect(
  #  users.create_login_url(
  #    get_next_url(request, default_url=url_for('dashboard'))))

def logout():
  flask_login.logout_user()
  return redirect(
    users.create_logout_url(
      get_next_url(request, default_url=url_for('index'))))
