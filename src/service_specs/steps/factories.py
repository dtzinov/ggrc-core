import factory
import random

def random_string(prefix=''):
  return '{prefix}{suffix}'.format(
      prefix=prefix,
      suffix=random.randint(0,9999999999),
      )

class SlugFactory(factory.Factory):
  ABSTRACT_FACTORY = True
  slug = factory.LazyAttribute(lambda m: random_string('slug'))
  title = factory.LazyAttribute(lambda m: random_string('title'))

class ControlFactory(SlugFactory):
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


