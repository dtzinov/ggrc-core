from ggrc import db
from ggrc.models import Control
from tests.ggrc import TestCase
from .factories import CategoryFactory, ControlFactory

class TestControl(TestCase):
  def test_simple_categorization(self):
    category = CategoryFactory()
    control = ControlFactory()
    control.categories.append(category)
    db.session.commit()
    self.assertIn(category, control.categories)
    # be really really sure
    control = db.session.query(Control).get(control.id)
    self.assertIn(category, control.categories)
