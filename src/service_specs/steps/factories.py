import datetime
import factory
import random
from factory.fuzzy import FuzzyChoice, FuzzyDateTime
from factory.compat import UTC

def random_string(prefix=''):
  return '{prefix}{suffix}'.format(
      prefix=prefix,
      suffix=random.randint(0,9999999999),
      )

def random_string_attribute(prefix=''):
  return factory.LazyAttribute(lambda m: random_string(prefix))

class DescribedFactory(factory.Factory):
  ABSTRACT_FACTORY = True
  description = random_string_attribute('description ')

class HyperlinkedFactory(factory.Factory):
  ABSTRACT_FACTORY = True
  # No properties to contribute by default, just useful for mirroring the class
  # hierarchy

class SluggedFactory(factory.Factory):
  ABSTRACT_FACTORY = True
  slug = random_string_attribute('slug')
  title = random_string_attribute('title')

class TimeboxedFactory(factory.Factory):
  ABSTRACT_FACTORY = True
  start_date = FuzzyDateTime(
      datetime.datetime(2000,1,1,tzinfo=UTC),
      datetime.datetime(2013,1,1,tzinfo=UTC),
      )
  end_date = FuzzyDateTime(
      datetime.datetime(2013,1,1,tzinfo=UTC),
      datetime.datetime.now(UTC) + datetime.timedelta(days=730),
      )

class BusinessObjectFactory(
    DescribedFactory, HyperlinkedFactory, SluggedFactory):
  ABSTRACT_FACTORY = True

class ControlFactory(SluggedFactory):
  FACTORY_FOR = dict
  #directive_id = None
  #type_id = None
  #kind_id = None
  version = None
  documentation_description = None
  #verify_frequency_id = None
  fraud_related = None
  key_control = None
  active = None
  notes = None

class ProgramFactory(BusinessObjectFactory, TimeboxedFactory):
  FACTORY_FOR = dict
  kind = FuzzyChoice(['Directive', 'Company Controls'])

