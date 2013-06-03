
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

"""Settings for Flask and Flask-SQLAlchemy

Flask: http://flask.pocoo.org/docs/config/
Flask-SQLAlchemy: https://github.com/mitsuhiko/flask-sqlalchemy/blob/master/docs/config.rst

Default settings should go in `settings.default`.

Environment/deployment-specific settings should go in `settings.<environment_name>`.
"""

import sys, os

BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
MODULE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
SETTINGS_DIR = os.path.join(BASE_DIR, 'ggrc', 'settings')

from default import *

settings_modules = os.environ.get("GGRC_SETTINGS_MODULE", '')

if len(settings_modules.strip()) == 0:
  raise RuntimeError(
    "Specify your settings using the `GGRC_SETTINGS_MODULE` environment variable")

for module_name in settings_modules.split(" "):
  if len(module_name.strip()) == 0:
    continue

  #logging.info("Loading settings file: %s" % module_name)

  filename = "%s.py" % module_name
  fullpath = os.path.join(SETTINGS_DIR, filename)

  try:
    execfile(fullpath)
  except Exception, e:
    raise

#logging.info("SQLALCHEMY_DATABASE_URI: %s" % locals().get("SQLALCHEMY_DATABASE_URI", None))