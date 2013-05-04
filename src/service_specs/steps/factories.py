import datetime
import factory
import random
from factory.base import BaseFactory, FactoryMetaClass, CREATE_STRATEGY
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyDateTime, FuzzyInteger
from factory.compat import UTC
from ggrc import models
from ggrc.models.reflection import AttributeInfo

def random_string(prefix=''):
  return '{prefix}{suffix}'.format(
      prefix=prefix,
      suffix=random.randint(0,9999999999),
      )

def random_string_attribute(prefix=''):
  return factory.LazyAttribute(lambda m: random_string(prefix))

class FactoryAttributeGenerator(object):
  @classmethod
  def generate(cls, attrs, model_class, attr):
    if (hasattr(attr, '__call__')):
      attr_name = attr.attr_name
      value = []
    else:
      attr_name = attr
      class_attr = getattr(model_class, attr_name)
      method = getattr(cls, class_attr.__class__.__name__)
      value = method(attr_name, class_attr)
    attrs[attr_name] = value

  @classmethod
  def InstrumentedAttribute(cls, attr_name, class_attr):
    method = getattr(cls, class_attr.property.__class__.__name__)
    return method(attr_name, class_attr)

  @classmethod
  def ColumnProperty(cls, attr_name, class_attr):
    method = getattr(
        cls,
        class_attr.property.expression.type.__class__.__name__,
        cls.default_column_handler)
    return method(attr_name, class_attr)

  @classmethod
  def default_column_handler(cls, attr_name, class_attr):
    return random_string_attribute(attr_name)

  @classmethod
  def DateTime(cls, attr_name, class_attr):
    return FuzzyDateTime(
      datetime.datetime(2013,1,1,tzinfo=UTC),
      datetime.datetime.now(UTC) + datetime.timedelta(days=730),
      )

  @classmethod
  def Date(cls, attr_name, class_attr):
    return FuzzyDate(
      datetime.date(2013,1,1),
      datetime.date.today() + datetime.timedelta(days=730),
      )

  @classmethod
  def Boolean(cls, attr_name, class_attr):
    return FuzzyChoice([True, False])

  @classmethod
  def Integer(cls, attr_name, class_attr):
    return FuzzyInteger(0,100000)

  @classmethod
  def RelationshipProperty(cls, attr_name, class_attr):
    if class_attr.property.uselist:
      return []
    else:
      return None

  @classmethod
  def AssociationProxy(cls, attr_name, class_attr):
    return []

class ModelFactoryMetaClass(FactoryMetaClass):
  def __new__(cls, class_name, bases, attrs, extra_attrs=None):
    model_class = attrs.pop('MODEL', None)
    if model_class:
      attrs['FACTORY_FOR'] = dict
      attribute_info = AttributeInfo(model_class)
      for attr in attribute_info._create_attrs:
        if hasattr(attr, '__call__'):
          attr_name = attr.attr_name
        else:
          attr_name = attr
        if not hasattr(cls, attr_name):
          FactoryAttributeGenerator.generate(attrs, model_class, attr)
    return super(ModelFactoryMetaClass, cls).__new__(
        cls, class_name, bases, attrs)

ModelFactory = ModelFactoryMetaClass(
    'ModelFactory', (BaseFactory,), {
    'ABSTRACT_FACTORY': True,
    'FACTORY_STRATEGY': CREATE_STRATEGY,
    '__doc__': """ModelFactory base with build and create support.

    This class has supports SQLAlchemy ORM.
    """,
    })

class CategoryFactory(ModelFactory):
  MODEL = models.Category

class ControlFactory(ModelFactory):
  MODEL = models.Control

class CycleFactory(ModelFactory):
  MODEL = models.Cycle

class DirectiveFactory(ModelFactory):
  MODEL = models.Directive

class DataAssetFactory(ModelFactory):
  MODEL = models.DataAsset

class ProgramFactory(ModelFactory):
  MODEL = models.Program
  kind = FuzzyChoice(['Directive', 'Company Controls'])
