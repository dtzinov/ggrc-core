"""ModelInflection
* handles various naming lookups for models
* can override based on model class variables
"""

import re

class ModelInflector(object):
  def __new__(cls, model):
    try:
      return _inflectors[cls]
    except KeyError:
      inflector = super(ModelInflector, cls).__new__(cls, model)
      _inflectors[model] = inflector
      return inflector

  def __init__(self, model):
    self.model = model
    register_inflections(self)

  def all_inflections(self):
    return {
      'model_singular': self.model_singular,
      'model_plural': self.model_plural,
      'table_singular': self.table_singular,
      'table_plural': self.table_plural,
      'human_singular': self.human_singular,
      'human_plural': self.human_plural,
      'title_singular': self.title_singular,
      'title_plural': self.title_plural,
      }

  @property
  def model_singular(self):
    return self.model.__name__

  @property
  def model_plural(self):
    return self.title_plural.replace(' ', '')

  @property
  def table_singular(self):
    return self.underscore_from_camelcase(self.model_singular)

  @property
  def table_plural(self):
    return self.model.__tablename__

  @property
  def human_singular(self):
    return self.title_singular.lower()

  @property
  def human_plural(self):
    return self.title_plural.lower()

  @property
  def title_singular(self):
    return self.titleize_from_camelcase(self.model.__name__)

  @property
  def title_plural(self):
    return self.model.__tablename__.replace('_', ' ').title()

  # Helpers
  @classmethod
  def underscore_from_camelcase(cls, s):
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

  @classmethod
  def titleize_from_camelcase(cls, s):
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1 \2', s)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', s1)

  def __repr__(self):
    return (
      'ModelInflector({model}):\n'
      '  model: {model_singular} {model_plural}\n'
      '  table: {table_singular} {table_plural}\n'
      '  human: {human_singular} {human_plural}\n'
      '  title: {title_singular} {title_plural}\n')\
      .format(model=self.model, **self.all_inflections())

class ModelInflectorDescriptor(object):
  cache_attribute = '_cached_inflector'

  def __get__(self, obj, cls):
    model_inflector = getattr(cls, self.cache_attribute, None)
    if model_inflector is None:
      model_inflector = ModelInflector(cls)
      setattr(cls, self.cache_attribute, model_inflector)
    return model_inflector


# { <model class>: <ModelInflector()> }
_inflectors = {}

# { <inflection>: <model class> }
_inflection_to_model = {}

def register_inflections(inflector):
  for mode, value in inflector.all_inflections().items():
    _inflection_to_model[value] = inflector.model

def get_model(s):
  return _inflection_to_model[s]
