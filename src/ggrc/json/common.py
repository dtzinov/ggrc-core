import ggrc.json
import ggrc.services

def url_for(obj):
  service = getattr(ggrc.services, obj.__class__.__name__)
  return service.url_for(obj)

def get_json_builder(obj):
  return getattr(ggrc.json, obj.__class__.__name__, None)

def publish(obj):
  publisher = get_json_builder(obj)
  if publisher:
    ret = {
        'id': obj.id,
        'selfLink': url_for(obj),
        'created_at': obj.created_at,
        'updated_at': obj.updated_at,
        }
    ret.update(publisher.publish_contribution(obj))
    return ret
  # Otherwise, just return the value itself by default
  return obj

def update(obj, json_obj):
  updater = get_json_builder(obj)
  if updater:
    updater.update(obj, json_obj)
  #FIXME what to do if no updater??
  #Nothing, perhaps log, assume omitted by design

def create(obj, json_obj):
  creator = get_json_builder(obj)
  if creator:
    creator.create(obj, json_obj)

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
  _publish_attrs = []
  _update_attrs = None # If None, same as _publish_attrs by default
  _create_attrs = None # If None, same as _update_attrs by default

  @classmethod
  def publish_attrs(cls, obj, json_obj):
    for a in cls._publish_attrs:
      json_obj[a] = publish(getattr(obj, a))

  @classmethod
  def get_update_attrs(cls):
    return cls._update_attrs or cls._publish_attrs

  @classmethod
  def get_create_attrs(cls):
    return cls._create_attrs or cls.get_update_attrs()

  @classmethod
  def do_update_attrs(cls, obj, json_obj, attrs):
    #TODO deal with nested objects
    for a in attrs:
      setattr(obj, a, json_obj.get(a))

  @classmethod
  def update_attrs(cls, obj, json_obj):
    cls.do_update_attrs(obj, json_obj, cls.get_update_attrs())

  @classmethod
  def create_attrs(cls, obj, json_obj):
    cls.do_update_attrs(obj, json_obj, cls.get_create_attrs())

  @classmethod
  def publish_base_contributions(cls, obj, json_obj, bases):
    for base in bases:
      if hasattr(ggrc.json, base.__name__):
        getattr(ggrc.json, base.__name__).publish_attrs(obj, json_obj)
        cls.publish_base_contributions(obj, json_obj, base.__bases__)

  @classmethod
  def publish_contribution(cls, obj):
    json_obj = {}
    cls.publish_attrs(obj, json_obj)
    cls.publish_base_contributions(obj, json_obj, obj.__class__.__bases__)
    return json_obj

  @classmethod
  def do_base_updates(cls, obj, json_obj, bases, update=True):
    for base in bases:
      builder = getattr(ggrc.json, base.__name__, None)
      if builder:
        if update:
          builder.update_attrs(obj, json_obj)
        else:
          builder.create_attrs(obj, json_obj)
        cls.do_base_updates(obj, json_obj, base.__bases__, update)

  @classmethod
  def update(cls, obj, json_obj):
    cls.update_attrs(obj, json_obj)
    cls.do_base_updates(obj, json_obj, obj.__class__.__bases__)

  @classmethod
  def create(cls, obj, json_obj):
    cls.create_attrs(obj, json_obj)
    cls.do_base_updates(obj, json_obj, obj.__class__.__bases__, False)

