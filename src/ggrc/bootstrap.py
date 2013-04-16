import sys
sys.path.insert(0, 'packages.zip')

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask('ggrc', instance_relative_config=True)
app.config.from_object('ggrc.settings.default')
app.config.from_pyfile('settings.cfg')

db = SQLAlchemy(app)
