import os
import threading
from ggrc import db
from ggrc.app import app

from wsgiref.simple_server import make_server

def before_all(context):
  settings_module = os.environ.get('GGRC_SETTINGS_MODULE', '')
  if not settings_module or settings_module == ' ':
    os.environ['GGRC_SETTINGS_MODULE'] = 'testing'
  context.base_url = 'http://localhost:8000'
  db.create_all()
  app.debug = False
  app.testing = True
  context.server = make_server('', 8000, app)
  context.thread = threading.Thread(target=context.server.serve_forever)
  context.thread.start()

def after_all(context):
  context.server.shutdown()
  context.thread.join()
  db.session.remove()
  db.drop_all()
