from ggrc.app import db, app

"""ggrc.views
Handle non-RESTful views, e.g. routes which return HTML rather than JSON
"""

# Additional template filters
#

@app.template_filter("underscore")
def underscore_filter(s):
  """Change spaces to underscores and make lowercase
  """
  return "_".join(s.lower().split(' '))

@app.template_filter("nospace")
def nospace_filter(s):
  """Remove spaces
  """
  return "".join(s.split(' '))

@app.context_processor
def inject_config():
    return dict(config=app.config)

from flask import render_template

# Actual HTML-producing routes
#

@app.route("/")
def hello():
  """The initial entry point of the app
  """
  return render_template("welcome/index.haml")

@app.route("/login")
def login():
  """The login page
  """
  return render_template("user_sessions/login.html")

@app.route("/dashboard")
def dashboard():
  """The dashboard page
  """
  return render_template("dashboard/index.haml")

@app.route("/design")
def styleguide():
  '''The style guide page
  '''
  return render_template("styleguide.haml")


def all_object_views():
  object_views = [
    'programs',
    'directives',
    'cycles',
    'controls',
    'systems',
    'products',
    'org_groups',
    'facilities',
    'markets',
    'projects',
    'data_assets',
    'risky_attributes',
    'risks',
    'people',
    'pbc_lists',
    ]

  import ggrc.services
  collections = dict(ggrc.services.all_collections())

  def with_model(object_plural):
    return (object_plural, collections.get(object_plural))

  return map(with_model, object_views)

def init_all_object_views(app):
  from .common import BaseObjectView

  for k,v in all_object_views():
    BaseObjectView.add_to(app, '/{}'.format(k), v)
