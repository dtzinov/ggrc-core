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

@app.route("/programs_dash")
def programs_dash():
  """The dashboard page
  """
  return render_template("programs_dash/index.haml")

@app.route("/design")
def styleguide():
  '''The style guide page
  '''
  return render_template("styleguide.haml")
