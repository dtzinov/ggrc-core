from flask.ext.testing import TestCase as BaseTestCase
from ggrc import db, app

class TestCase(BaseTestCase):
  def setUp(self):
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def create_app(self):
    app.testing = True
    app.debug = False
    return app
