
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from ggrc.models import Control
from tests.ggrc import TestCase
from .factories import CategoryFactory, ControlFactory

class TestControl(TestCase):
  def test_simple_categorization(self):
    category = CategoryFactory(scope_id=100)
    control = ControlFactory()
    control.categories.append(category)
    db.session.commit()
    self.assertIn(category, control.categories)
    # be really really sure
    control = db.session.query(Control).get(control.id)
    self.assertIn(category, control.categories)