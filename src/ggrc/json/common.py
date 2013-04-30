import ggrc.json
import ggrc.services

CACHE_BUILDERS = True

def url_for(obj):
  service = getattr(ggrc.services, obj.__class__.__name__, None)
  return service.url_for(obj) if service else None

def get_json_builder(obj):
  if type(obj) is type:
    cls = obj
  else:
    cls = obj.__class__
  builder = getattr(ggrc.json, cls.__name__, None)
  if not builder:
    builder = Builder(cls)
    setattr(ggrc.json, cls.__name__, builder)
  return builder

def publish(obj):
  publisher = get_json_builder(obj)
  if publisher and publisher._publish_attrs:
    url = url_for(obj)
    ret = {'selfLink': url_for(obj)} if url else {}
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
  def __init__(self, tgt_class):
    self._publish_attrs = Builder.gather_publish_attrs(tgt_class)
    self._update_attrs = Builder.gather_update_attrs(tgt_class)
    self._create_attrs = Builder.gather_create_attrs(tgt_class)

  @classmethod
  def gather_attrs(cls, tgt_class, src_attrs, accumulator=None):
    src_attrs = src_attrs if type(src_attrs) is list else [src_attrs]
    accumulator = accumulator if accumulator is not None else []
    for attr in src_attrs:
      attrs = getattr(tgt_class, attr, None)
      if attrs is not None:
        accumulator.extend(attrs)
        break
    for base in tgt_class.__bases__:
      cls.gather_attrs(base, src_attrs, accumulator)
    return accumulator

  @classmethod
  def gather_publish_attrs(cls, tgt_class):
    return cls.gather_attrs(tgt_class, '_publish_attrs')

  @classmethod
  def gather_update_attrs(cls, tgt_class):
    return cls.gather_attrs(tgt_class, ['_update_attrs', '_publish_attrs'])

  @classmethod
  def gather_create_attrs(cls, tgt_class):
    return cls.gather_attrs(tgt_class, [
      '_create_attrs', '_update_attrs', '_publish_attrs'])

  def publish_attrs(self, obj, json_obj):
    for a in self._publish_attrs:
      json_obj[a] = publish(getattr(obj, a))

  @classmethod
  def do_update_attrs(cls, obj, json_obj, attrs):
    #TODO deal with nested objects
    for a in attrs:
      setattr(obj, a, json_obj.get(a))

  def update_attrs(self, obj, json_obj):
    self.do_update_attrs(obj, json_obj, self._update_attrs)

  def create_attrs(self, obj, json_obj):
    self.do_update_attrs(obj, json_obj, self._create_attrs)

  def publish_contribution(self, obj):
    json_obj = {}
    self.publish_attrs(obj, json_obj)
    return json_obj

  def update(self, obj, json_obj):
    self.update_attrs(obj, json_obj)

  def create(self, obj, json_obj):
    self.create_attrs(obj, json_obj)
