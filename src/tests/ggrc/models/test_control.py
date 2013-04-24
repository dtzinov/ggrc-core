import factory
import random
from flask.ext.testing import TestCase
from ggrc import app, db
from ggrc.models import Categorization, Category, Control

def random_string(prefix=''):
  return '{prefix}{suffix}'.format(
      prefix=prefix,
      suffix=random.randint(0,9999999999),
      )

class ModelFactory(factory.Factory):
  ABSTRACT_FACTORY = True
  modified_by_id = 1

  @classmethod
  def _create(cls, target_class, *args, **kwargs):
    instance = target_class(*args, **kwargs)
    db.session.add(instance)
    db.session.commit()
    return instance

class SlugFactory(factory.Factory):
  ABSTRACT_FACTORY = True
  slug = factory.LazyAttribute(lambda m: random_string('slug'))
  title = factory.LazyAttribute(lambda m: random_string('title'))

class ControlFactory(ModelFactory, SlugFactory):
  FACTORY_FOR = Control
  directive_id = None
  type_id = None
  kind_id = None
  version = None
  documentation_description = None
  verify_frequency_id = None
  fraud_related = None
  key_control = None
  active = None
  notes = None

class CategoryFactory(ModelFactory):
  FACTORY_FOR = Category
  name = factory.LazyAttribute(lambda m: random_string('name'))
  lft = None
  rgt = None
  scope_id = None
  depth = None
  required = None

class CategorizationFactory(ModelFactory):
  FACTORY_FOR = Categorization
  category = None
  categorizable = None
  category_id = None
  categorizable_id = None
  categorizable_type = None

class TestControl(TestCase):
  def setUp(self):
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def create_app(self):
    app.testing = True
    app.debug = False
    return app

  def test_simple_categorization(self):
    category = CategoryFactory()
    control = ControlFactory()
    control.categories.append(category)
    db.session.commit()
    self.assertIn(category, control.categories)
    # be really really sure
    control = db.session.query(Control).get(control.id)
    self.assertIn(category, control.categories)
