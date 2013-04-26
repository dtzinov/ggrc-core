import ggrc.json
import ggrc.services

def url_for(obj):
  service = getattr(ggrc.services, obj.__class__.__name__)
  return service.url_for(obj)

def build(obj):
  ret = {
      'id': obj.id,
      'selfLink': url_for(obj),
      'created_at': obj.created_at,
      'updated_at': obj.updated_at,
      }
  builder = getattr(ggrc.json, obj.__class__.__name__)
  ret.update(builder.build_contribution(obj))
  return ret

class Builder(object):
  '''JSON Dictionary builder for ggrc.models.* objects and their mixins.

  Builder classes can override the `_simple_attrs` class attribute with a list
  of attribute names to be extracted from a model instance and included into
  the dictionary for the json representation of the object.

  Builder classes can also override the `_build_contribution` class method.

  A Builder class should be defined for __every__ ggrc.model class and mixin.
  Mixin inheritance is respected - the base classes will be walked and any
  Builder for that class will be run and have it's contributions to the
  dictionary recorded.
  '''
  _simple_attrs = []

  @classmethod
  def add_simple_attrs(cls, obj, json_obj):
    for a in cls._simple_attrs:
      json_obj[a] = getattr(obj, a)

  @classmethod
  def _build_contribution(cls, ob):
    return {}

  @classmethod
  def do_build_contribution(cls, obj, json_obj):
    json_obj.update(cls._build_contribution(obj))
    cls.add_simple_attrs(obj, json_obj)
    return json_obj

  @classmethod
  def build_base_contributions(cls, obj, json_obj, bases):
    for base in bases:
      if hasattr(ggrc.json, base.__name__):
        getattr(ggrc.json, base.__name__).do_build_contribution(obj, json_obj)
        cls.build_base_contributions(obj, json_obj, base.__bases__)

  @classmethod
  def build_contribution(cls, obj):
    json_obj = {}
    cls.do_build_contribution(obj, json_obj)
    cls.build_base_contributions(obj, json_obj, obj.__class__.__bases__)
    return json_obj
