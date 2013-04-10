import sys
sys.path.insert(0, 'packages.zip')

from flask import Flask

app = Flask('ggrc', instance_relative_config=True)
app.config.from_object('ggrc.settings.default')
app.config.from_pyfile('settings.cfg')

@app.route("/")
def hello():
  return 'Hello World!'
