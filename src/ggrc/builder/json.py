# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

import ggrc.builder
import ggrc.services
import iso8601
from datetime import datetime
from flask import _request_ctx_stack, request
from ggrc import db
from ggrc.models.reflection import AttributeInfo
from ggrc.services.util import url_for
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import RelationshipProperty
from werkzeug.exceptions import BadRequest

"""JSON resource state representation handler for gGRC models."""

def view_url_for(obj):
  view = getattr(ggrc.views, obj.__class__.__name__, None)
  return view.url_for(obj) if view else None

def get_json_builder(obj):
  """Instantiate or retrieve a JSON representation builder for the given
  object.
  """
  if type(obj) is type:
    cls = obj
  else:
    cls = obj.__class__
  # Lookup the builder instance in the builder module
  builder = getattr(ggrc.builder, cls.__name__, None)
  if not builder:
    # Create the builder and cache it in the builder module
    builder = Builder(cls)
    setattr(ggrc.builder, cls.__name__, builder)
  return builder

def publish(obj):
  """Translate ``obj`` into a valid JSON value. Objects with properties are
  translated into a ``dict`` object representing a JSON object while simple
  values are returned unchanged or specially formatted if needed.
  """
  publisher = get_json_builder(obj)
  if publisher and hasattr(publisher, '_publish_attrs') \
      and publisher._publish_attrs:
    ret = {}
    self_url = url_for(obj)
    if self_url:
      ret['selfLink'] = self_url
    view_url = view_url_for(obj)
    if view_url:
      ret['viewLink'] = view_url
    ret.update(publisher.publish_contribution(obj))
    return ret
  # Otherwise, just return the value itself by default
  return obj

def update(obj, json_obj):
  """Translate the state represented by ``json_obj`` into update actions
  performed upon the model object ``obj``. After performing the update ``obj``
  and ``json_obj`` should be equivalent representations of the model state.
  """
  updater = get_json_builder(obj)
  if updater:
    updater.update(obj, json_obj)
  #FIXME what to do if no updater??
  #Nothing, perhaps log, assume omitted by design

def create(obj, json_obj):
  """Translate the state represented by ``json_obj`` into update actions
  performed upon the new model object ``obj``. After performing the update
  ``obj`` and ``json_obj`` should be equivalent representations of the model
  state.
  """
  creator = get_json_builder(obj)
  if creator:
    creator.create(obj, json_obj)

class UpdateAttrHandler(object):
  """Performs the translation of a JSON state representation into update
  actions performed on a model object instance.
  """
  @classmethod
  def do_update_attr(cls, obj, json_obj, attr):
    """Perform the update to ``obj`` required to make the attribute attr
    equivalent in ``obj`` and ``json_obj``.
    """
    if (hasattr(attr, '__call__')):
      # The attribute has been decorated with a callable, grab the name and
      # invoke the callable to get the value
      attr_name = attr.attr_name
      value = attr(cls, obj, json_obj)
    else:
      # Lookup the method to use to perform the update. Use reflection to
      # key off of the type of the attribute and invoke the method of the
      # same name.
      attr_name = attr
      class_attr = getattr(obj.__class__, attr_name)
      method = getattr(cls, class_attr.__class__.__name__)
      value = method(obj, json_obj, attr_name, class_attr)
    setattr(obj, attr_name, value)

  @classmethod
  def InstrumentedAttribute(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for an ``InstrumentedAttribute``"""
    method = getattr(cls, class_attr.property.__class__.__name__)
    return method(obj, json_obj, attr_name, class_attr)

  @classmethod
  def ColumnProperty(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a ``ColumnProperty``"""
    method = getattr(
        cls,
        class_attr.property.expression.type.__class__.__name__,
        cls.default_column_handler)
    return method(obj, json_obj, attr_name, class_attr)

  @classmethod
  def default_column_handler(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a simple value column"""
    return json_obj.get(attr_name)

  @classmethod
  def DateTime(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a ``Datetime`` column."""
    value = json_obj.get(attr_name)
    try:
      return iso8601.parse_date(value) if value else None
    except iso8601.ParseError as e:
      raise BadRequest(
          'Malformed DateTime {0} for parameter {1}. '
          'Error message was: {2}'.format(value, attr_name, e.message)
          )

  @classmethod
  def Date(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a ``Date`` column."""
    value = json_obj.get(attr_name)
    try:
      return datetime.strptime(value, "%Y-%m-%d") if value else None
    except ValueError as e:
      raise BadRequest(
          'Malformed Date {0} for parameter {1}. '
          'Error message was: {2}'.format(value, attr_name, e.message)
          )

  @classmethod
  def query_for(cls, rel_class, json_obj, attr_name, uselist):
    """Resolve the model object instance referred to by the JSON value."""
    if uselist:
      # The value is a collection of links, resolve the collection of objects
      value = json_obj.get(attr_name)
      rel_ids = [o[u'id'] for o in value] if value else []
      if rel_ids:
        return db.session.query(rel_class).filter(
            rel_class.id.in_(rel_ids)).all()
      else:
        return []
    else:
      rel_obj = json_obj.get(attr_name)
      if rel_obj:
        try:
          return db.session.query(rel_class).filter(
            rel_class.id == rel_obj[u'id']).one()
        except(TypeError):
          raise TypeError(''.join(['Failed to convert attribute ', attr_name]))
      return None

  @classmethod
  def RelationshipProperty(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for a ``RelationshipProperty``."""
    rel_class = class_attr.property.mapper.class_
    return cls.query_for(
        rel_class, json_obj, attr_name, class_attr.property.uselist)

  @classmethod
  def AssociationProxy(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for an ``AssociationProxy``."""
    rel_class = class_attr.remote_attr.property.mapper.class_
    return cls.query_for(rel_class, json_obj, attr_name, True)

  @classmethod
  def property(cls, obj, json_obj, attr_name, class_attr):
    """Translate the JSON value for an object method decorated as a
    ``property``.
    """
    #FIXME need a way to decide this. Require link? Use URNs?
    #  reflective approaches won't work as this is used for polymorphic
    #  properties
    # rel_class = None
    # return cls.query_for(rel_class, json_obj, attr_name, True)
    if attr_name in json_obj:
      url = json_obj[attr_name]['href']
      rel_class_name = _request_ctx_stack.top.url_adapter.match(url, 'GET')[0]
      from ggrc import models
      rel_class = getattr(models, rel_class_name)
      return cls.query_for(rel_class, json_obj, attr_name, False)
    return None

class Builder(AttributeInfo):
  """JSON Dictionary builder for ggrc.models.* objects and their mixins."""

  def generate_link_object_for(self, obj):
    return {'id': obj.id, 'href': url_for(obj)}

  def publish_link_collection(self, obj, json_obj, attr_name):
    """The ``attr_name`` attribute is a collection of object references;
    translate the collection of object references into a collection of link
    objects for the JSON dictionary representation.
    """
    return [self.generate_link_object_for(o) for o in getattr(obj, attr_name)]

  def publish_link(self, obj, json_obj, attr_name):
    """The ``attr_name`` attribute is an object reference; translate the object
    reference into a link object for the JSON dictionary representation.
    """
    attr_value = getattr(obj, attr_name)
    if attr_value:
      return self.generate_link_object_for(attr_value)
    return None

  def publish_attrs(self, obj, json_obj):
    """Translate the state represented by ``obj`` into the JSON dictionary
    ``json_obj``.
    """
    for attr in self._publish_attrs:
      if hasattr(attr, '__call__'):
        attr_name = attr.attr_name
      else:
        attr_name = attr
      class_attr = getattr(obj.__class__, attr_name)
      if isinstance(class_attr, AssociationProxy):
        json_obj[attr_name] = self.publish_link_collection(
            obj, json_obj, attr_name)
      elif isinstance(class_attr, InstrumentedAttribute) and \
           isinstance(class_attr.property, RelationshipProperty):
        if class_attr.property.uselist:
          json_obj[attr_name] = self.publish_link_collection(
              obj, json_obj, attr_name)
        else:
          json_obj[attr_name] = self.publish_link(obj, json_obj, attr_name)
      elif isinstance(class_attr, property):
        json_obj[attr_name] = self.publish_link(obj, json_obj, attr_name)
      else:
        json_obj[attr_name] = getattr(obj, attr_name)

  @classmethod
  def do_update_attrs(cls, obj, json_obj, attrs):
    """Translate every attribute in ``attrs`` from the JSON dictionary value
    to a value or model object instance for references set for the attribute
    in ``obj``.
    """
    for attr_name in attrs:
      UpdateAttrHandler.do_update_attr(obj, json_obj, attr_name)

  def update_attrs(self, obj, json_obj):
    """Translate the state representation given by ``json_obj`` into the
    model object ``obj``.
    """
    self.do_update_attrs(obj, json_obj, self._update_attrs)

  def create_attrs(self, obj, json_obj):
    """Translate the state representation given by ``json_obj`` into the new
    model object ``obj``.
    """
    self.do_update_attrs(obj, json_obj, self._create_attrs)

  def publish_contribution(self, obj):
    """Translate the state represented by ``obj`` into a JSON dictionary"""
    json_obj = {}
    self.publish_attrs(obj, json_obj)
    return json_obj

  def update(self, obj, json_obj):
    """Update the state represented by ``obj`` to be equivalent to the state
    represented by the JSON dictionary ``json_obj``.
    """
    self.update_attrs(obj, json_obj)

  def create(self, obj, json_obj):
    """Update the state of the new model object ``obj`` to be equivalent to the
    state represented by the JSON dictionary ``json_obj``.
    """
    self.create_attrs(obj, json_obj)
