import datetime
import factory
import random
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyDateTime
from factory.compat import UTC

def random_string(prefix=''):
  return '{prefix}{suffix}'.format(
      prefix=prefix,
      suffix=random.randint(0,9999999999),
      )

def random_string_attribute(prefix=''):
  return factory.LazyAttribute(lambda m: random_string(prefix))

class ChangeTrackedFactory(factory.Factory):
  ABSTRACT_FACTORY = True

class DescribedFactory(factory.Factory):
  ABSTRACT_FACTORY = True
  description = random_string_attribute('description ')

class HyperlinkedFactory(factory.Factory):
  ABSTRACT_FACTORY = True
  # No properties to contribute by default, just useful for mirroring the class
  # hierarchy

class IdentifiableFactory(factory.Factory):
  ABSTRACT_FACTORY = True

class BaseFactory(IdentifiableFactory, ChangeTrackedFactory):
  FACTORY_FOR = dict

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

class HierarchicalFactory(factory.Factory):
  ABSTRACT_FACTORY = True

class CategoryFactory(BaseFactory, HierarchicalFactory):
  FACTORY_FOR = dict
  name = random_string_attribute('name')
  required = FuzzyChoice([True, False])

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

class CycleFactory(BaseFactory, DescribedFactory):
  FACTORY_FOR = dict
  start_at = FuzzyDate(
      datetime.date(2000,1,1),
      datetime.date(2013,1,1),
      )
  complete = FuzzyChoice([True,False])
  title = random_string_attribute('title')
  audit_firm = random_string_attribute('some firm, LLC ')
  audit_lead = random_string_attribute('Some One, ')
  status = random_string_attribute('status')
  notes = random_string_attribute('notes')
  end_at = FuzzyDate(
      datetime.date(2013,1,1),
      datetime.date.today() + datetime.timedelta(days=730),
      )
  report_due_at =  FuzzyDate(
      datetime.date(2013,1,1),
      datetime.date.today() + datetime.timedelta(days=730),
      )

class DirectiveFactory(SluggedFactory, HyperlinkedFactory, TimeboxedFactory):
  FACTORY_FOR = dict
  company = FuzzyChoice([True,False])
  version = random_string_attribute('version ')
  organization = random_string_attribute('organization ')
  scope = random_string_attribute('scope ')
  audit_start_date = FuzzyDateTime(
      datetime.datetime(2000,1,1,tzinfo=UTC),
      datetime.datetime.now(UTC),
      )
  programs = []

class DataAssetFactory(TimeboxedFactory, BusinessObjectFactory):
  FACTORY_FOR = dict

class ProgramFactory(BusinessObjectFactory, TimeboxedFactory):
  FACTORY_FOR = dict
  kind = FuzzyChoice(['Directive', 'Company Controls'])

