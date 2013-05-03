import ggrc.json
import ggrc.services
from datetime import datetime
from ggrc import db
from iso8601 import parse_date
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm.properties import RelationshipProperty

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
  if publisher and hasattr(publisher, '_publish_attrs') \
      and publisher._publish_attrs:
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

class UpdateAttrHandler(object):
  @classmethod
  def do_update_attr(cls, obj, json_obj, attr_name):
    class_attr = getattr(obj.__class__, attr_name)
    method = getattr(cls, class_attr.__class__.__name__)
    value = method(obj, json_obj, attr_name, class_attr)
    setattr(obj, attr_name, value)

  @classmethod
  def InstrumentedAttribute(cls, obj, json_obj, attr_name, class_attr):
    method = getattr(cls, class_attr.property.__class__.__name__)
    return method(obj, json_obj, attr_name, class_attr)

  @classmethod
  def ColumnProperty(cls, obj, json_obj, attr_name, class_attr):
    method = getattr(
        cls,
        class_attr.property.expression.type.__class__.__name__,
        cls.default_column_handler)
    return method(obj, json_obj, attr_name, class_attr)

  @classmethod
  def default_column_handler(cls, obj, json_obj, attr_name, class_attr):
    return json_obj.get(attr_name)

  @classmethod
  def DateTime(cls, obj, json_obj, attr_name, class_attr):
    value = json_obj.get(attr_name)
    return parse_date(value) if value else None

  @classmethod
  def Date(cls, obj, json_obj, attr_name, class_attr):
    value = json_obj.get(attr_name)
    return datetime.strptime(value, "%Y-%m-%d") if value else None

  @classmethod
  def RelationshipProperty(cls, obj, json_obj, attr_name, class_attr):
    rel_class = class_attr.property.mapper.class_
    if class_attr.property.uselist:
      value = json_obj.get(attr_name)
      rel_ids = [o.id for o in value] if value else []
      return db.session.query(rel_class).filter(
          rel_class.id.in_(rel_ids)).all()
    else:
      rel_obj = json_obj.get(attr_name)
      if rel_obj:
        return db.session.query(rel_class).filter(
            rel_class.id == rel_obj.id).one()
      return None

  @classmethod
  def AssociationProxy(cls, obj, json_obj, attr_name, class_attr):
    rel_class = class_attr.remote_attr.property.mapper.class_
    value = json_obj.get(attr_name)
    rel_ids = [o[u'id'] for o in value] if value else []
    return db.session.query(rel_class).filter(rel_class.id.in_(rel_ids)).all()

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
    accumulator = accumulator if accumulator is not None else set()
    for attr in src_attrs:
      attrs = tgt_class.__dict__.get(attr, None)
      if attrs is not None:
        accumulator.update(attrs)
        break
    for base in tgt_class.__bases__:
      cls.gather_attrs(base, src_attrs, accumulator)
    return accumulator

  @classmethod
  def gather_publish_attrs(cls, tgt_class):
    return cls.gather_attrs(tgt_class, '_publish_attrs')

  @classmethod
  def gather_update_attrs(cls, tgt_class):
    attrs = cls.gather_attrs(tgt_class, ['_update_attrs', '_publish_attrs'])
    return attrs

  @classmethod
  def gather_create_attrs(cls, tgt_class):
    return cls.gather_attrs(tgt_class, [
      '_create_attrs', '_update_attrs', '_publish_attrs'])

  def publish_link_collection(self, obj, json_obj, attr_name):
    return [{'id': o.id, 'href': url_for(o)} for o in getattr(obj, attr_name)]

  def publish_link(self, obj, json_obj, attr_name):
    attr_value = getattr(obj, attr_name)
    if attr_value:
      return {'id': attr_value.id, 'href': url_for(attr_value)}
    return None

  def publish_attrs(self, obj, json_obj):
    for attr_name in self._publish_attrs:
      class_attr = getattr(obj.__class__, attr_name)
      if isinstance(class_attr, AssociationProxy):
        json_obj[attr_name] = self.publish_link_collection(
            obj, json_obj, attr_name)
      elif isinstance(class_attr.property, RelationshipProperty):
        if class_attr.property.uselist:
          json_obj[attr_name] = self.publish_link_collection(
              obj, json_obj, attr_name)
        else:
          json_obj[attr_name] = self.publish_link(obj, json_obj, attr_name)
      else:
        json_obj[attr_name] = getattr(obj, attr_name)

  @classmethod
  def do_update_attrs(cls, obj, json_obj, attrs):
    for attr_name in attrs:
      UpdateAttrHandler.do_update_attr(obj, json_obj, attr_name)

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

