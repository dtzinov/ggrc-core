# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import threading
from ggrc import db
from ggrc.app import app
from ggrc.models import create_db, drop_db
from wsgiref.simple_server import make_server

use_migrations = False

def before_all(context):
  context.base_url = 'http://localhost:8000'
  create_db(use_migrations)
  app.debug = False
  app.testing = True
  context.server = make_server('', 8000, app)
  context.thread = threading.Thread(target=context.server.serve_forever)
  context.thread.start()

def after_all(context):
  context.server.shutdown()
  context.thread.join()
  db.session.remove()
  drop_db(use_migrations)
