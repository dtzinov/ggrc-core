from flask.ext.testing import TestCase as BaseTestCase
from ggrc import db
from ggrc.app import app
from ggrc.models import create_db, drop_db

use_migrations = False

class TestCase(BaseTestCase):
  def setUp(self):
    create_db(use_migrations, quiet=True)

  def tearDown(self):
    db.session.remove()
    drop_db(use_migrations, quiet=True)

  def create_app(self):
    app.testing = True
    app.debug = False
    return app
